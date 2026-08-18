import ast
import tempfile
from pathlib import Path

import streamlit as st
from radon.complexity import cc_visit

from core.parser.parser import PythonParser
from core.analysis.security import SecurityAnalyzer
from app.pages.history import add_analysis_history


# =========================================================
# COMPLEXITY
# =========================================================

def _calculate_complexity(code):

    try:

        blocks = cc_visit(code)

        if not blocks:
            return {
                "average": 0.0,
                "highest": 0,
                "functions": 0,
                "blocks": [],
            }

        complexities = [
            block.complexity
            for block in blocks
        ]

        return {
            "average": round(
                sum(complexities) / len(complexities),
                2,
            ),
            "highest": max(complexities),
            "functions": len(blocks),
            "blocks": blocks,
        }

    except Exception:

        return {
            "average": 0.0,
            "highest": 0,
            "functions": 0,
            "blocks": [],
        }


# =========================================================
# CODE SMELLS
# =========================================================

def _detect_code_smells(code):

    smells = []

    try:
        tree = ast.parse(code)

    except SyntaxError:
        return smells

    for node in ast.walk(tree):

        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):

            end_line = getattr(
                node,
                "end_lineno",
                node.lineno,
            )

            length = (
                end_line
                - node.lineno
                + 1
            )

            if length > 60:

                smells.append(
                    {
                        "type": "Large Function",
                        "line": node.lineno,
                        "message": (
                            f"{node.name}() contains "
                            f"{length} lines"
                        ),
                    }
                )

        if isinstance(
            node,
            ast.ExceptHandler,
        ):

            if node.type is None:

                smells.append(
                    {
                        "type": "Bare Except",
                        "line": node.lineno,
                        "message": (
                            "Bare except detected"
                        ),
                    }
                )

        if isinstance(node, ast.Global):

            smells.append(
                {
                    "type": "Global Statement",
                    "line": node.lineno,
                    "message": (
                        "Global statement detected"
                    ),
                }
            )

        if isinstance(node, ast.Call):

            if isinstance(
                node.func,
                ast.Name,
            ):

                if node.func.id == "print":

                    smells.append(
                        {
                            "type": "Print Statement",
                            "line": node.lineno,
                            "message": (
                                "print() detected"
                            ),
                        }
                    )

    return smells


# =========================================================
# QUALITY SCORE
# =========================================================

def _quality_score(
    documentation,
    complexity,
    security_score,
    smells,
):

    documentation_score = documentation

    if complexity <= 5:
        complexity_score = 100

    elif complexity <= 10:
        complexity_score = 80

    elif complexity <= 20:
        complexity_score = 60

    else:
        complexity_score = 40

    smell_penalty = min(
        len(smells) * 5,
        30,
    )

    smell_score = 100 - smell_penalty

    score = (
        documentation_score * 0.20
        + complexity_score * 0.25
        + security_score * 0.35
        + smell_score * 0.20
    )

    return round(
        max(
            0,
            min(100, score),
        ),
        1,
    )


# =========================================================
# MAIN PAGE
# =========================================================

def show_paste():

    st.title("Paste Code")

    st.caption(
        "Paste Python code and run a complete static analysis."
    )

    code = st.text_area(
        "Python Code",
        height=280,
        placeholder=(
            "Paste your Python code here..."
        ),
    )

    analyze_button = st.button(
        "Analyze Code",
        type="primary",
        use_container_width=True,
    )

    if not analyze_button:
        return

    if not code.strip():

        st.warning(
            "Please paste some Python code first."
        )

        return

    temp_path = None

    try:

        # =================================================
        # TEMP FILE
        # =================================================

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8",
        ) as temp_file:

            temp_file.write(code)

            temp_path = temp_file.name

        # =================================================
        # PARSER
        # =================================================

        parser = PythonParser()

        result = parser.parse(
            Path(temp_path)
        )

        # =================================================
        # COMPLEXITY
        # =================================================

        complexity = _calculate_complexity(
            code
        )

        # =================================================
        # SECURITY
        # =================================================

        security_analyzer = SecurityAnalyzer()

        security_result = security_analyzer.analyze(
            Path(temp_path)
        )

        security_score = security_result.get(
            "score",
            100,
        )

        security_issues = security_result.get(
            "issues",
            [],
        )

        # =================================================
        # CODE SMELLS
        # =================================================

        smells = _detect_code_smells(
            code
        )

        # =================================================
        # FUNCTIONS
        # =================================================

        functions = getattr(
            result,
            "functions",
            [],
        )

        total_functions = len(
            functions
        )

        documented_functions = sum(
            1
            for function in functions
            if getattr(
                function,
                "docstring",
                None,
            )
        )

        if total_functions:

            documentation = round(
                (
                    documented_functions
                    / total_functions
                )
                * 100,
                1,
            )

        else:

            documentation = 100.0

        # =================================================
        # CLASSES
        # =================================================

        classes = getattr(
            result,
            "classes",
            [],
        )

        # =================================================
        # QUALITY
        # =================================================

        quality = _quality_score(
            documentation,
            complexity["average"],
            security_score,
            smells,
        )

        # =================================================
        # HISTORY
        # =================================================

        add_analysis_history(
            analysis_type="Paste Code",
            name="Pasted Python Code",
            quality_score=quality,
            security_score=security_score,
            complexity=complexity["average"],
            functions=total_functions,
            classes=len(classes),
            code_smells=len(smells),
        )

        # =================================================
        # SUCCESS
        # =================================================

        st.success(
            "Code analysis completed successfully."
        )

        # =================================================
        # MAIN METRICS
        # =================================================

        st.subheader("Analysis Overview")

        c1, c2, c3, c4, c5 = st.columns(5)

        with c1:
            st.metric(
                "Quality",
                f"{quality}/100",
            )

        with c2:
            st.metric(
                "Security",
                f"{security_score}/100",
            )

        with c3:
            st.metric(
                "Complexity",
                complexity["average"],
            )

        with c4:
            st.metric(
                "Functions",
                total_functions,
            )

        with c5:
            st.metric(
                "Code Smells",
                len(smells),
            )

        st.divider()

        # =================================================
        # TABS
        # =================================================

        overview_tab, security_tab, complexity_tab, quality_tab, structure_tab, ai_tab = st.tabs(
            [
                "📊 Overview",
                "🛡️ Security",
                "📈 Complexity",
                "🧹 Code Quality",
                "🧩 Structure",
                "🤖 AI Summary",
            ]
        )

        # =================================================
        # OVERVIEW
        # =================================================

        with overview_tab:

            st.subheader(
                "Parser Analysis"
            )

            p1, p2, p3, p4 = st.columns(4)

            with p1:

                st.metric(
                    "Total Lines",
                    getattr(
                        result,
                        "total_lines",
                        0,
                    ),
                )

            with p2:

                st.metric(
                    "Functions",
                    total_functions,
                )

            with p3:

                st.metric(
                    "Classes",
                    len(classes),
                )

            with p4:

                st.metric(
                    "Imports",
                    len(
                        getattr(
                            result,
                            "imports",
                            [],
                        )
                    ),
                )

            syntax_error = getattr(
                result,
                "syntax_error",
                False,
            )

            if syntax_error:

                st.error(
                    "Syntax Error Detected"
                )

                message = getattr(
                    result,
                    "syntax_error_message",
                    None,
                )

                if message:
                    st.code(message)

            else:

                st.success(
                    "No Python syntax errors detected."
                )

            st.subheader(
                "Quality Summary"
            )

            q1, q2, q3 = st.columns(3)

            with q1:

                st.metric(
                    "Documentation",
                    f"{documentation}%",
                )

            with q2:

                st.metric(
                    "Documented Functions",
                    documented_functions,
                )

            with q3:

                st.metric(
                    "Code Smells",
                    len(smells),
                )

        # =================================================
        # SECURITY
        # =================================================

        with security_tab:

            st.subheader(
                "Security Analysis"
            )

            s1, s2 = st.columns(2)

            with s1:

                st.metric(
                    "Security Score",
                    f"{security_score}/100",
                )

            with s2:

                st.metric(
                    "Issues Detected",
                    len(security_issues),
                )

            if not security_issues:

                st.success(
                    "No security issues detected."
                )

            else:

                st.warning(
                    f"{len(security_issues)} "
                    "security issue(s) detected."
                )

                for issue in security_issues:

                    severity = issue.get(
                        "severity",
                        "Unknown",
                    )

                    issue_type = issue.get(
                        "type",
                        "Security Issue",
                    )

                    line = issue.get(
                        "line",
                        "N/A",
                    )

                    message = issue.get(
                        "message",
                        "",
                    )

                    with st.expander(
                        f"{severity} • {issue_type} • Line {line}"
                    ):

                        st.write(message)

        # =================================================
        # COMPLEXITY
        # =================================================

        with complexity_tab:

            st.subheader(
                "Cyclomatic Complexity"
            )

            c1, c2, c3 = st.columns(3)

            with c1:

                st.metric(
                    "Average",
                    complexity["average"],
                )

            with c2:

                st.metric(
                    "Highest",
                    complexity["highest"],
                )

            with c3:

                st.metric(
                    "Functions Analyzed",
                    complexity["functions"],
                )

            if complexity["blocks"]:

                for block in complexity["blocks"]:

                    value = block.complexity

                    if value <= 5:
                        level = "Low"

                    elif value <= 10:
                        level = "Moderate"

                    else:
                        level = "High"

                    st.write(
                        f"**{block.name}** — "
                        f"Complexity **{value}** "
                        f"({level})"
                    )

            else:

                st.info(
                    "No function complexity information available."
                )

        # =================================================
        # CODE QUALITY
        # =================================================

        with quality_tab:

            st.subheader(
                "Code Quality"
            )

            st.metric(
                "Overall Quality Score",
                f"{quality}/100",
            )

            st.divider()

            q1, q2, q3 = st.columns(3)

            with q1:

                st.metric(
                    "Documentation",
                    f"{documentation}%",
                )

            with q2:

                st.metric(
                    "Security",
                    f"{security_score}/100",
                )

            with q3:

                st.metric(
                    "Code Smells",
                    len(smells),
                )

            st.divider()

            st.subheader(
                "Detected Code Smells"
            )

            if not smells:

                st.success(
                    "No obvious code smells detected."
                )

            else:

                for smell in smells:

                    with st.expander(
                        f"{smell['type']} • Line {smell['line']}"
                    ):

                        st.write(
                            smell["message"]
                        )

            st.subheader(
                "Documentation"
            )

            st.progress(
                documentation / 100
            )

            st.caption(
                f"{documented_functions} of "
                f"{total_functions} functions documented."
            )

        # =================================================
        # STRUCTURE
        # =================================================

        with structure_tab:

            st.subheader(
                "Project Structure"
            )

            imports = getattr(
                result,
                "imports",
                [],
            )

            with st.expander(
                f"📦 Imports ({len(imports)})",
                expanded=False,
            ):

                if imports:

                    for item in imports:

                        st.write(
                            f"- {item}"
                        )

                else:

                    st.info(
                        "No imports detected."
                    )

            with st.expander(
                f"⚙️ Functions ({len(functions)})",
                expanded=False,
            ):

                if functions:

                    for function in functions:

                        name = getattr(
                            function,
                            "name",
                            "Unknown",
                        )

                        line = getattr(
                            function,
                            "line_number",
                            getattr(
                                function,
                                "lineno",
                                "-",
                            ),
                        )

                        st.write(
                            f"**{name}** — "
                            f"Line {line}"
                        )

                else:

                    st.info(
                        "No functions detected."
                    )

            with st.expander(
                f"🏛️ Classes ({len(classes)})",
                expanded=False,
            ):

                if classes:

                    for cls in classes:

                        name = getattr(
                            cls,
                            "name",
                            "Unknown",
                        )

                        line = getattr(
                            cls,
                            "line_number",
                            getattr(
                                cls,
                                "lineno",
                                "-",
                            ),
                        )

                        st.write(
                            f"**{name}** — "
                            f"Line {line}"
                        )

                else:

                    st.info(
                        "No classes detected."
                    )

            todo_count = getattr(
                result,
                "todo_count",
                0,
            )

            fixme_count = getattr(
                result,
                "fixme_count",
                0,
            )

            st.subheader(
                "TODO / FIXME"
            )

            t1, t2 = st.columns(2)

            with t1:

                st.metric(
                    "TODO",
                    todo_count,
                )

            with t2:

                st.metric(
                    "FIXME",
                    fixme_count,
                )

        # =================================================
        # AI SUMMARY
        # =================================================

        with ai_tab:

            st.subheader(
                "AI Code Summary"
            )

            st.caption(
                "Generate an AI-powered explanation of your code."
            )

            if st.button(
                "Generate AI Summary",
                key="paste_ai_summary",
                use_container_width=True,
            ):

                try:

                    from core.ai.summarizer import summarizer

                    with st.spinner(
                        "Gemini is analyzing the code..."
                    ):

                        summary = summarizer.summarize(
                            code,
                            "Python",
                        )

                    st.markdown(summary)

                except Exception as e:

                    st.error(
                        f"AI Error: {e}"
                    )

    except Exception as e:

        st.error(
            "Code analysis failed."
        )

        st.exception(e)

    finally:

        if temp_path:

            try:

                Path(temp_path).unlink(
                    missing_ok=True
                )

            except Exception:

                pass
