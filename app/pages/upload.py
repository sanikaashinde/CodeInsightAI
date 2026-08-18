from pathlib import Path
import streamlit as st

from core.utils.file_loader import FileLoader
from core.utils.project_scanner import scan_project
from core.utils.language_detector import detect_language
from core.parser.parser import PythonParser
from core.analysis.complexity import ComplexityAnalyzer
from core.analysis.smells import SmellDetector
from core.analysis.summarizer import AISummarizer
from app.pages.project_dashboard import show_project_dashboard
from app.components.dependency_graph import show_dependency_graph
from app.pages.history import add_analysis_history
from core.analysis.security import SecurityAnalyzer

loader = FileLoader()
parser = PythonParser()
complexity = ComplexityAnalyzer()
smells = SmellDetector()
summarizer = AISummarizer()

security = SecurityAnalyzer()


def calculate_quality_score(
    documentation,
    complexity,
    security_score,
    smells,
):
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
        30
    )

    smell_score = 100 - smell_penalty

    score = (
        documentation * 0.20
        + complexity_score * 0.25
        + security_score * 0.35
        + smell_score * 0.20
    )

    return round(
        max(0, min(100, score)),
        1
    )


def show_upload():

    st.title("Upload Project")

    uploaded_files = st.file_uploader(
        "Upload code files or ZIP project",
        accept_multiple_files=True,
        type=[
            "py", "java", "cpp", "c", "js", "ts",
            "jsx", "tsx", "go", "rs", "php", "rb",
            "cs", "swift", "kt", "html", "css",
            "json", "xml", "yaml", "yml", "zip"
        ]
    )

    if not uploaded_files:
        st.info("Upload one or more source files or a ZIP project.")
        return

    total_files = 0

    for uploaded in uploaded_files:

        saved = loader.save_uploaded_file(uploaded)

        st.write(saved)

        if saved.suffix.lower() == ".zip":

            project_folder = loader.extract_zip(saved)

            print(project_folder)

            st.write(project_folder)
            st.write("Project Folder:", project_folder)

            if project_folder is None:
                st.error("extract_zip() returned None")
                st.stop()

            show_project_dashboard(project_folder)

            scan_result = scan_project(project_folder)

            files = scan_result.get("files", [])

            show_dependency_graph(project_folder)

        else:

            files = [saved]

        st.success(f"Uploaded: {saved.name}")

        for file in files:

            file = Path(file)

            total_files += 1

            language = detect_language(file)

            with st.expander(file.name):

                if language != "Python":
                    st.info(f"Skipped from deep analysis: {file.name} ({language}). Deep static analysis is currently focused on Python projects.")
                    continue

                try:

                    analysis = parser.parse(file)

                    code = file.read_text(
                        encoding="utf-8",
                        errors="ignore"
                    )

                    complexity_result = complexity.analyze(code)

                    smell_result = smells.detect(analysis)


                    # --------------------------------------------------
                    # SAVE COMPLETE FILE ANALYSIS TO HISTORY
                    # --------------------------------------------------

                    upload_complexity = complexity_result.get(
                        "average_complexity",
                        0
                    )

                    upload_functions = complexity_result.get(
                        "total_functions",
                        len(analysis.functions)
                    )

                    upload_classes = len(
                        analysis.classes
                    )

                    upload_smells = len(
                        smell_result
                    )

                    # -------------------------------------------------
                    # DOCUMENTATION SCORE
                    # -------------------------------------------------

                    upload_functions_list = getattr(
                        analysis,
                        "functions",
                        []
                    )

                    documented_functions = sum(
                        1
                        for function in upload_functions_list
                        if getattr(
                            function,
                            "docstring",
                            None
                        )
                    )

                    total_functions = len(
                        upload_functions_list
                    )

                    if total_functions:
                        documentation = round(
                            (
                                documented_functions
                                / total_functions
                            ) * 100,
                            1
                        )
                    else:
                        documentation = 100.0

                    # -------------------------------------------------
                    # SECURITY ANALYSIS
                    # -------------------------------------------------

                    security_result = security.analyze(file)

                    upload_security = security_result.get(
                        "score",
                        100
                    )

                    # -------------------------------------------------
                    # QUALITY SCORE
                    # -------------------------------------------------

                    upload_quality = calculate_quality_score(
                        documentation=documentation,
                        complexity=upload_complexity,
                        security_score=upload_security,
                        smells=smell_result,
                    )

                    # -------------------------------------------------
                    # SAVE UPLOAD HISTORY
                    # -------------------------------------------------

                    add_analysis_history(
                        analysis_type="Upload Project",
                        name=file.name,
                        quality_score=upload_quality,
                        security_score=upload_security,
                        complexity=upload_complexity,
                        functions=upload_functions,
                        classes=upload_classes,
                        code_smells=upload_smells,
                    )
                    # -------------------------------------------------
                    # OVERALL QUALITY
                    # -------------------------------------------------

                    st.subheader("Overall Code Quality")

                    q1, q2, q3, q4 = st.columns(4)

                    q1.metric(
                        "Quality Score",
                        f"{upload_quality}/100"
                    )

                    q2.metric(
                        "Documentation",
                        f"{documentation}%"
                    )

                    q3.metric(
                        "Security",
                        f"{upload_security}/100"
                    )

                    q4.metric(
                        "Code Smells",
                        upload_smells
                    )

                    st.divider()

                    c1, c2, c3 = st.columns(3)

                    c1.metric(
                        "Language",
                        analysis.language
                    )

                    c2.metric(
                        "Lines",
                        analysis.total_lines
                    )

                    c3.metric(
                        "Functions",
                        len(analysis.functions)
                    )


                    # ---------------- Security Analysis ----------------

                    st.subheader("Security Analysis")

                    security_score = security_result.get("score", 100)
                    security_issues = security_result.get("issues", [])

                    sc1, sc2 = st.columns(2)

                    sc1.metric(
                        "Security Score",
                        f"{security_score}/100"
                    )

                    sc2.metric(
                        "Security Issues",
                        len(security_issues)
                    )

                    if security_issues:

                        st.warning(
                            f"{len(security_issues)} security issue(s) detected."
                        )

                        for issue in security_issues:

                            severity = issue.get("severity", "Unknown")
                            issue_type = issue.get("type", "Security Issue")
                            line = issue.get("line", "N/A")
                            message = issue.get("message", "")

                            st.write(
                                f"**{severity} - {issue_type}** | "
                                f"Line: {line} | {message}"
                            )

                    else:

                        st.success("No security issues detected.")

                    st.divider()

                    st.divider()

                    # ---------------- Imports ----------------

                    st.subheader("Imports")

                    if analysis.imports:

                        for item in analysis.imports:
                            st.write(f"- {item}")

                    else:

                        st.info("No imports found.")

                    # ---------------- Classes ----------------

                    st.subheader("Classes")

                    if analysis.classes:

                        for cls in analysis.classes:

                            st.markdown(
                                f"### {cls.name}"
                            )

                            st.write(
                                f"**Inheritance:** "
                                f"{', '.join(cls.bases) if cls.bases else 'None'}"
                            )

                            st.write(
                                f"**Methods:** "
                                f"{', '.join(cls.methods) if cls.methods else 'None'}"
                            )

                            st.write(
                                f"**Line:** {cls.line_number}"
                            )

                            if cls.docstring:
                                st.code(cls.docstring)

                            st.markdown("---")

                    else:

                        st.info("No classes found.")

                    # ---------------- Complexity ----------------

                    st.subheader("Cyclomatic Complexity")

                    if complexity_result:

                        c1, c2, c3 = st.columns(3)

                        c1.metric(
                            "Average Complexity",
                            complexity_result.get(
                                "average_complexity",
                                0
                            )
                        )

                        c2.metric(
                            "Highest Complexity",
                            complexity_result.get(
                                "highest_complexity",
                                0
                            )
                        )

                        c3.metric(
                            "Functions Analyzed",
                            complexity_result.get(
                                "total_functions",
                                0
                            )
                        )

                        st.divider()

                        functions = complexity_result.get(
                            "functions",
                            []
                        )

                        if functions:

                            for item in functions:

                                st.write(
                                    f"**{item['name']}** ? "
                                    f"Complexity **{item['complexity']}** "
                                    f"({item['rank']}) "
                                    f" Line {item['line']}"
                                )

                        else:

                            st.info(
                                "No function-level complexity information available."
                            )

                    else:

                        st.info(
                            "No complexity information available."
                        )

                    # ---------------- Code Smells ----------------

                    st.subheader("Code Smells")

                    if smell_result:

                        for smell in smell_result:

                            st.warning(
                                f"{smell['type']} ? "
                                f"{smell['function']}"
                            )

                    else:

                        st.success(
                            "No obvious code smells detected."
                        )

                    # ---------------- AI Summary ----------------

                    st.divider()

                    st.subheader("AI Analysis")

                    if st.button(
                        "Generate AI Summary",
                        key=f"summary_{file.stem}"
                    ):

                        with st.spinner(
                            "Gemini is analyzing the code..."
                        ):

                            try:

                                summary = summarizer.summarize(
                                    code,
                                    language
                                )

                                st.markdown(summary)

                            except Exception as e:

                                st.error(
                                    f"AI Error: {e}"
                                )

                except Exception as e:

                    st.error(
                        f"Analysis Error: {e}"
                    )

    st.success(f"Total files analyzed: {total_files}")














