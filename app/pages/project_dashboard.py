import streamlit as st
import pandas as pd

# ==========================================================
# CORE ANALYSIS
# ==========================================================

from core.analysis.project_analyzer import ProjectAnalyzer
from core.analysis.project_summary import ProjectSummary
from core.analysis.project_ai_review import AIProjectReview
from core.analysis.project_health import ProjectHealth
from core.analysis.quality_score import ProjectQualityScore
from core.analysis.complexity import ComplexityAnalyzer
from core.analysis.security import SecurityAnalyzer

from core.analysis.repository_search import RepositorySearch
from core.analysis.dependency_graph import DependencyGraph
from core.analysis.call_graph import FunctionCallGraph
from core.analysis.duplicate_detector import DuplicateCodeDetector

from core.analysis.dead_code import DeadCodeAnalyzer
from core.analysis.todo_detector import TodoDetector
from core.analysis.repository_statistics import RepositoryStatistics
from core.analysis.repository_insights import RepositoryInsights
from core.analysis.architecture_visualizer import ArchitectureVisualizer

# ==========================================================
# PARSER
# ==========================================================

from core.parser.parser import PythonParser

# ==========================================================
# EXPORT
# ==========================================================

from core.export.pdf_exporter import PDFExporter
from core.export.readme_generator import ReadmeGenerator

# ==========================================================
# COMPONENTS
# ==========================================================

from app.components.project_chat import show_project_chat
from app.components.repository_chat import show_repository_chat
from app.components.repository_search import show_repository_search
from app.components.dependency_graph import show_dependency_graph
from app.components.call_graph import show_call_graph
from app.components.duplicate_detector import show_duplicate_detector
from app.components.code_metrics_dashboard import (
    show_code_metrics_dashboard,
)
from app.components.technical_debt import show_technical_debt
from core.analysis.technical_debt import TechnicalDebtAnalyzer
# ==========================================================
# INITIALIZE OBJECTS
# ==========================================================

parser = PythonParser()

scanner = ProjectAnalyzer()

summary = ProjectSummary()

reviewer = AIProjectReview()

health = ProjectHealth()

quality = ProjectQualityScore()

complexity = ComplexityAnalyzer()

security = SecurityAnalyzer()

pdf_exporter = PDFExporter()

readme_generator = ReadmeGenerator()

repo_search = RepositorySearch()

dependency = DependencyGraph()

call_graph = FunctionCallGraph()

duplicate_detector = DuplicateCodeDetector()

dead_code = DeadCodeAnalyzer()

todo_scanner = TodoDetector()

repository_stats = RepositoryStatistics()

repository_insights = RepositoryInsights()

architecture = ArchitectureVisualizer()

technical_debt = TechnicalDebtAnalyzer()

# ==========================================================
# PROJECT DASHBOARD
# ==========================================================


def show_project_dashboard(project_folder):

    project = scanner.scan(project_folder)

    analyses = []

    complexities = []

    security_results = []

    progress = st.progress(0)

    total = max(
        project.get("file_count", len(project.get("files", []))),
        1
    )

    # ======================================================
    # Parse Project
    # ======================================================

    for index, file in enumerate(project["files"]):

        progress.progress((index + 1) / total)

        try:

            analysis = parser.parse(file)

            analyses.append(analysis)

            try:

                code = file.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )

            except Exception:

                code = ""

            complexities.append(

                complexity.analyze(code)

            )

            security_results.append(

                security.analyze(file)

            )

        except Exception:

            continue

    progress.empty()

    # ======================================================
    # Core Summaries
    # ======================================================

    project_summary = summary.summarize(analyses)
    project_summary["total_files"] = len(analyses)
    project_summary["source_files"] = len(analyses)

    # Count every file in the uploaded project, including data,
    # database, model, image, configuration and documentation files.
    ignored = {
        ".git", ".venv", "__pycache__", "node_modules",
        ".idea", ".vscode", "env", "venv", "build", "dist",
        ".pytest_cache", ".mypy_cache"
    }

    all_project_files = [
        path
        for path in project_folder.rglob("*")
        if path.is_file()
        and not any(part in ignored for part in path.parts)
    ]

    project_summary["total_files"] = len(all_project_files)

    stats, libraries = health.analyze(
        analyses
    )

    scores = quality.calculate(
        analyses
    )

    technical_debt_result = technical_debt.analyze(
        project_folder,
        analyses,
    )

    repository = repository_stats.analyze(
        project_folder
    )

    dead_issues = dead_code.analyze(project_folder)

    dead_stats = dead_code.summary(dead_issues)

    dead = {
        "unused": dead_issues,
        "summary": {
            "functions": dead_stats["unused_functions"],
            "classes": dead_stats["empty_classes"],
            "variables": dead_stats["unused_variables"],
            "imports": dead_stats["unused_imports"],
            "unreachable": dead_stats["unreachable_code"],
            "empty_functions": dead_stats["empty_functions"],
            "total": dead_stats["total"],
        },
    }

    todo_items = todo_scanner.scan(project_folder)

    todo_summary = todo_scanner.summary(todo_items)

    todos = {
        "items": todo_items,
        "summary": {
            "total": todo_summary["total"],
            "files": len(set(item["file"] for item in todo_items)),
        },
    }

    duplicate_result = duplicate_detector.analyze(
        project_folder
    )

    duplicate_summary = duplicate_result["summary"]

    duplicates = duplicate_result["duplicates"]

    architecture_result = architecture.analyze(
        project_folder
    )

    insights = repository_insights.analyze(

        project,

        analyses,

        complexities,

        security_results,

        scores,

    )

    # ======================================================
    # COMPLEXITY SUMMARY
    # ======================================================

    # ======================================================
    # PROJECT-LEVEL COMPLEXITY SUMMARY
    # Weighted average across all analyzed functions
    # ======================================================

    all_complexity_functions = []

    for result in complexities:

        if not isinstance(result, dict):
            continue

        all_complexity_functions.extend(
            result.get("functions", [])
        )

    if all_complexity_functions:

        total_complexity = sum(
            item.get("complexity", 0)
            for item in all_complexity_functions
        )

        avg_complexity = round(
            total_complexity / len(all_complexity_functions),
            2
        )

    else:

        avg_complexity = 0

    
    top_functions = []

    for item in complexities:

        top_functions.extend(

            item["functions"]

        )

    top_functions = sorted(

        top_functions,

        key=lambda x: x["complexity"],

        reverse=True,

    )[:10]

    # ======================================================
    # SECURITY SUMMARY
    # ======================================================

    if security_results:

        security_score = round(

            sum(
                s["score"]
                for s in security_results
            ) / len(security_results),

            2,

        )

    else:

        security_score = 100

    issues = []

    for security_result in security_results:

        issues.extend(

            security_result["issues"]

        )

    total_security_issues = len(issues)

    # ======================================================
    # HEADER
    # ======================================================

    st.title("🚀 CodeInsight AI")

    st.caption(
        "Enterprise Static Code Analysis Platform"
    )

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("📂 Total Files", project_summary["total_files"])

    m2.metric(
        "📝 Lines",
        repository["statistics"]["lines"]
    )

    m3.metric(
        "⚙️ Functions",
        project_summary["functions"]
    )

    m4.metric(
        "🏛️ Classes",
        project_summary["classes"]
    )

    st.divider()

    # ======================================================
    # PROJECT HEALTH
    # ======================================================

    st.subheader("📈 Project Health")

    h1, h2, h3, h4 = st.columns(4)

    h1.metric(
        "Docstrings",
        stats["docstrings"]
    )

    h2.metric(
        "Large Functions",
        stats["large_functions"]
    )

    h3.metric(
        "Async",
        stats["async_functions"]
    )

    h4.metric(
        "Imports",
        stats["imports"]
    )

    st.divider()

    # ======================================================
    # CODE COMPLEXITY
    # ======================================================

    st.subheader("§  Code Complexity")

    c1, c2 = st.columns(2)

    c1.metric(
        "Average Complexity",
        avg_complexity
    )

    if avg_complexity <= 5:

        c2.success("🟢 Low Complexity")

    elif avg_complexity <= 10:

        c2.warning("🟡 Moderate Complexity")

    else:

        c2.error("🔴 High Complexity")

    st.markdown("### 🔥 Top Complex Functions")

    if top_functions:

        rows = []

        for func in top_functions:

            rows.append({

                "Function": func["name"],

                "Complexity": func["complexity"],

                "Rank": func["rank"],

                "Line": func["lineno"]

            })

        st.dataframe(

            pd.DataFrame(rows),

            use_container_width=True,

            hide_index=True,

        )

    else:

        st.info(
            "No functions found."
        )

    st.divider()

    # ======================================================
    # SECURITY ANALYSIS
    # ======================================================

    st.subheader("🛡️ Security Analysis")

    s1, s2 = st.columns(2)

    s1.metric(

        "Security Score",

        f"{security_score}/100"

    )

    s2.metric(

        "Issues",

        total_security_issues

    )

    if security_score >= 90:

        st.success(
            "Excellent Security"
        )

    elif security_score >= 70:

        st.warning(
            "Moderate Security"
        )

    else:

        st.error(
            "Security Needs Improvement"
        )

    if issues:

        st.dataframe(

            pd.DataFrame(issues),

            hide_index=True,

            use_container_width=True,

        )

    else:

        st.success(
            "No security issues detected."
        )

    st.divider()

    # ======================================================
    # PROJECT QUALITY SCORE
    # ======================================================

    st.subheader(" Project Quality")

    overall = scores["overall"]

    if overall >= 90:

        st.success(
            f"🏆 Excellent ({overall}/100)"
        )

    elif overall >= 75:

        st.info(
            f"✅ Good ({overall}/100)"
        )

    elif overall >= 60:

        st.warning(
            f"  Needs Improvement ({overall}/100)"
        )

    else:

        st.error(
            f"❌ Poor ({overall}/100)"
        )

    q1, q2 = st.columns(2)

    with q1:

        st.metric(
            "Documentation",
            f"{scores['documentation']}%"
        )

        st.progress(
            scores["documentation"] / 100
        )

        st.metric(
            "Readability",
            f"{scores['readability']}%"
        )

        st.progress(
            scores["readability"] / 100
        )

    with q2:

        st.metric(
            "Maintainability",
            f"{scores['maintainability']}%"
        )

        st.progress(
            scores["maintainability"] / 100
        )

        st.metric(
            "Architecture",
            f"{scores['architecture']}%"
        )

        st.progress(
            scores["architecture"] / 100
        )

    st.divider()

    # ======================================================
    # ENTERPRISE METRICS DASHBOARD
    # ======================================================

# ======================================================
# ENTERPRISE METRICS DASHBOARD
# ======================================================

    st.subheader("📊 Repository Metrics")
    
    show_code_metrics_dashboard(
        scores,                  # quality
        security_score,          # security
        avg_complexity,          # complexity
        repository,              # repository
        {
            "summary": duplicate_summary,
            "duplicates": duplicates,
        },
        dead,
        todos,
    )   

    st.divider()

    # ======================================================
    # MOST USED LIBRARIES
    # ======================================================

    st.subheader("📦 Most Used Libraries")

    if libraries:

        library_table = []

        for lib, count in libraries:

            library_table.append({

                "Library": lib,

                "Used In Files": count

            })

        st.dataframe(

            pd.DataFrame(library_table),

            hide_index=True,

            use_container_width=True,

        )

    else:

        st.info("No imports detected.")

    st.divider()

    # ======================================================
    # REPOSITORY SEARCH
    # ======================================================

    st.subheader("🔍 Repository Search")

    try:

        show_repository_search(
            project_folder
        )

    except Exception as e:

        st.warning(
            f"Repository Search unavailable : {e}"
        )

    st.divider()

    # ======================================================
    # DEPENDENCY GRAPH
    # ======================================================

    st.subheader("🕸️ Dependency Graph")

    try:

        show_dependency_graph(
            project_folder
        )

    except Exception as e:

        st.warning(
            f"Dependency Graph unavailable : {e}"
        )

    st.divider()
    # ======================================================
    # FUNCTION CALL GRAPH
    # ======================================================

    st.divider()

    try:

        show_call_graph(
            project_folder
        ) 

    except Exception as e:

        st.warning(
            f"Function Call Graph unavailable: {e}"
        )

    # ======================================================
    # DUPLICATE CODE DETECTOR
    # ======================================================

    st.subheader("👯 Duplicate Code Detection")

    try:

        duplicate_result = duplicate_detector.analyze(
            project_folder
        )

        duplicates = duplicate_result.get(
            "duplicates",
            []
        )

        duplicate_summary = duplicate_result.get(
            "summary",
            {}
        )

        duplicate_pairs = duplicate_summary.get(
            "duplicate_pairs",
            0
        )

        highest_similarity = duplicate_summary.get(
            "highest_similarity",
            0
        )

        affected_files = duplicate_summary.get(
            "affected_files",
            0
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Duplicate Pairs",
            duplicate_pairs
        )

        c2.metric(
            "Highest Similarity",
            f"{highest_similarity}%"
        )

        c3.metric(
            "Affected Files",
            affected_files
        )

        if duplicates:

            st.warning(
                f"Found {duplicate_pairs} duplicate code pair(s)."
            )

            st.dataframe(
                pd.DataFrame(duplicates),
                hide_index=True,
                use_container_width=True,
            )

        else:

            st.success(
                "No duplicate code detected."
            )

    except Exception as e:

        st.warning(
            f"Duplicate Detector unavailable : {e}"
        )

    st.divider()

    # ======================================================
    # DEAD CODE DETECTION
    # ======================================================

    st.subheader("Dead Code Detection")

    dead_summary = dead["summary"]

    d1, d2, d3, d4 = st.columns(4)

    d1.metric(
        "Unused Functions",
        dead_summary["functions"]
    )

    d2.metric(
        "Empty Classes",
        dead_summary["classes"]
    )

    d3.metric(
        "Unreachable Code",
        dead_summary["unreachable"]
    )

    d4.metric(
        "Empty Functions",
        dead_summary["empty_functions"]
    )

    if dead["unused"]:

        st.dataframe(

            pd.DataFrame(dead["unused"]),

            use_container_width=True,

            hide_index=True,

        )

    else:

        st.success(
            "No dead code detected."
        )

    st.divider()

    # ======================================================
    # TODO / FIXME SCANNER
    # ======================================================

    st.subheader("📝 TODO / FIXME Scanner")

    todo_summary = todos["summary"]

    t1, t2 = st.columns(2)

    t1.metric(
        "Pending Items",
        todo_summary["total"]
    )

    t2.metric(
        "Files",
        todo_summary["files"]
    )

    if todos["items"]:

        st.dataframe(

            pd.DataFrame(todos["items"]),

            hide_index=True,

            use_container_width=True,

        )

    else:

        st.success(
            "No TODOs found."
        )

    st.divider()

    # ======================================================
    # ARCHITECTURE VISUALIZER
    # ======================================================

    st.subheader(" Project Architecture")

    summary_info = architecture_result["summary"]

    a1, a2, a3 = st.columns(3)

    a1.metric(
        "Files",
        project_summary["total_files"]
    )

    a2.metric(
        "Packages",
        summary_info["packages"]
    )

    a3.metric(
        "Modules",
        summary_info["modules"]
    )

    st.markdown("### 📂 Project Tree")

    st.code(

        "\n".join(
            architecture.folder_tree(
                architecture_result
            )
        ),

        language="text",

    )

    st.markdown("### 📦 Package Summary")

    st.dataframe(

        pd.DataFrame(

            architecture.package_summary(
                architecture_result
            )
        ),

        hide_index=True,

        use_container_width=True,

    )

    st.divider()

    # ======================================================
    # REPOSITORY INSIGHTS
    # ======================================================

    st.subheader("💡 Repository Insights")

    st.metric(

        "Largest File",

        repository["largest_files"][0]["file"] if repository["largest_files"] else "N/A"

    )

    st.write(

        f"**Lines :** {repository['largest_files'][0]['lines'] if repository['largest_files'] else 0}"

    )

    st.metric(

        "Most Complex File",

        insights["most_complex"]["file"]

    )

    st.write(

        f"Average Complexity : {insights['most_complex']['complexity']}"

    )

    st.metric(

        "Most Functions",

        insights["most_functions"]["file"]

    )

    st.write(

        insights["most_functions"]["count"]

    )

    st.metric(

        "Most Classes",

        insights["most_classes"]["file"]

    )

    st.write(

        insights["most_classes"]["count"]

    )

    st.metric(

        "Best Documentation",

        insights["best_documentation"]["file"]

    )

    st.write(

        f"{insights['best_documentation']['coverage']}% coverage"

    )

    st.divider()

    # ======================================================
    # AI PROJECT REVIEW
    # ======================================================

    st.subheader("🤖 AI Project Review")

    if "project_ai_review" not in st.session_state:
        st.session_state.project_ai_review = None

    if st.button(
        "🚀 Generate AI Review",
        use_container_width=True,
    ):

        with st.spinner("Analyzing repository..."):

            try:

                st.session_state.project_ai_review = reviewer.review(

                    project_folder.name,

                    analyses,

                )

            except Exception as e:

                st.error(f"AI Error : {e}")

    if st.session_state.project_ai_review:

        with st.expander(

            "📄 View AI Review",

            expanded=True,

        ):

            st.markdown(

                st.session_state.project_ai_review

            )

    else:

        st.info(
            "Generate an AI review to receive a complete assessment."
        )

    st.divider()

    # ======================================================
    # AI REPOSITORY CHAT
    # ======================================================

    st.subheader("💬 AI Repository Chat")

    try:

        show_repository_chat(
            project_folder
        )

    except Exception as e:

        st.warning(
            f"Repository Chat unavailable : {e}"
        )

    st.divider()

    # ======================================================
    # PROJECT CHAT
    # ======================================================

    st.subheader("§  Chat With Project")

    try:

        show_project_chat(
            project_folder
        )

    except Exception as e:

        st.warning(
            f"Project Chat unavailable : {e}"
        )

    st.divider()

    # ======================================================
    # README GENERATOR
    # ======================================================

    st.subheader("📝 README Generator")

    if st.button(

        "Generate Professional README",

        use_container_width=True,

    ):

        with st.spinner(
            "Generating README..."
        ):

            try:

                readme = readme_generator.generate(

                    project_name=project_folder.name,

                    project_summary=project_summary,

                    scores=scores,

                    analyses=analyses,

                )

                st.download_button(

                    "Download README.md",

                    data=readme,

                    file_name="README.md",

                    mime="text/markdown",

                    use_container_width=True,

                )

            except Exception as e:

                st.error(e)

    st.divider()

    # ======================================================
    # PDF EXPORT
    # ======================================================

    st.subheader("📄 Export Report")

    try:

        pdf = pdf_exporter.generate(

            project_name=project_folder.name,

            project=project,

            result=project_summary,

            stats=stats,

            scores=scores,

            analyses=analyses,

            ai_review=st.session_state.project_ai_review,

            security_score=security_score,

            security_issues=issues,

        )

        st.download_button(

            "“¥ Download Professional PDF",

            data=pdf,

            file_name=f"{project_folder.name}_CodeInsight_Report.pdf",

            mime="application/pdf",

            use_container_width=True,

        )

    except Exception as e:

        st.error(e)

    st.divider()

    st.divider()

    show_technical_debt(
        technical_debt_result
    )
    # ======================================================
    # FINAL ASSESSMENT
    # ======================================================


    st.subheader("🏆 Final Project Assessment")

    # ------------------------------------------------------
    # Supporting metrics
    # ------------------------------------------------------

    quality_score = float(
        scores.get("overall", 0)
)

    security_score_value = float(
        security_score
    )

    technical_debt_score = float(
        technical_debt_result.get("score", 0)
    )

    # Technical debt score is a risk/debt score:
    # lower debt = better project.
    debt_health = max(
        0,
        min(
            100,
            100 - technical_debt_score
        )
    )

    # Complexity health
    complexity_health = max(
        0,
        min(
            100,
            100 - (avg_complexity * 5)
        )
    )

    # ------------------------------------------------------
    # Production readiness
    # ------------------------------------------------------

    production = round(
        (
            quality_score * 0.50
            + security_score_value * 0.25
            + debt_health * 0.15
            + complexity_health * 0.10
        ),
        1
    )

    production = max(
        0,
        min(100, production)
    )

    # ------------------------------------------------------
    # Internship readiness
    # ------------------------------------------------------

    documentation_score = float(
        scores.get("documentation", 0)
    )

    architecture_score = float(
        scores.get("architecture", 0)
    )

    maintainability_score = float(
        scores.get("maintainability", 0)
    )

    internship = round(
        (
            quality_score * 0.35
            + documentation_score * 0.15
            + architecture_score * 0.15
            + maintainability_score * 0.15
            + security_score_value * 0.10
            + debt_health * 0.10
        ),
        1
    )

    internship = max(
        0,
        min(100, internship)
    )

    # ------------------------------------------------------
    # Display
    # ------------------------------------------------------

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "Production Ready",
            f"{production}%"
        )

        st.progress(
            production / 100
        )

    with c2:

        st.metric(
            "Internship Ready",
            f"{internship}%"
        )

        st.progress(
            internship / 100
        )

    st.divider()

    # ======================================================
    # FINAL RECOMMENDATION
    # ======================================================

    st.subheader("Final Recommendation")

    if production >= 90:

        st.success(
            """
    ### Enterprise Ready

    ✅ Excellent overall quality

    ✅ Strong architecture

    ✅ Strong Security

    Production Ready

    Resume Ready

    Portfolio Ready

    ✅Internship Ready

    """
        )

    elif production >= 75:

        st.info(
            """
    ### ✅ Strong Project

    • Good Architecture

    • Good Maintainability

    • Good Security

    • Minor Improvements Remaining

    - Ready for Resume

    - Ready for Internship
    """
        )

    elif production >= 60:

        st.warning(
            """

    ###   Needs Improvement

    • Some quality improvements are required

    • Core project is functional

    • Documentation should be improved

    • Technical debt should be reduced
    
    • Further testing is recommended
    """
        )

    else:

        st.error(
            """
    ### ❌ Significant Improvements Required

    • Project quality is below the recommended level

    • Documentation needs improvement

    • Code quality requires attention

    • Security and maintainability should be reviewed

    • Additional testing is recommended
    """
        )       

    # ======================================================
    # FOOTER
    # ======================================================

    st.caption(

        "🚀 CodeInsight AI v3.0 | Enterprise Static Code Analysis Platform | Built with Python • Streamlit • AST • Radon"

    )


















