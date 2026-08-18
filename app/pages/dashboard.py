import streamlit as st

from core.auth import get_analysis_history


def show_dashboard():

    # =====================================================
    # HEADER
    # =====================================================

    st.title("CodeInsight AI")

    st.caption(
        "AI-powered Python code analysis, security scanning and project insights."
    )

    st.divider()

    # =====================================================
    # WELCOME
    # =====================================================

    st.subheader(
        f"Welcome back, {st.session_state.user['full_name']} 👋"
    )

    st.write(
        "Analyze your codebase, identify quality and security issues, "
        "understand complexity, and get actionable insights from one place."
    )

    st.divider()

    # =====================================================
    # OVERVIEW
    # =====================================================

    st.subheader("Your Analysis Overview")

    user = st.session_state.get("user")

    if user:
        history = get_analysis_history(user["id"])
    else:
        history = []

    total_analyses = len(history)

    quality_values = [
        item.get("quality_score")
        for item in history
        if item.get("quality_score") is not None
    ]

    security_values = [
        item.get("security_score")
        for item in history
        if item.get("security_score") is not None
    ]

    smell_values = [
        item.get("code_smells")
        for item in history
        if item.get("code_smells") is not None
    ]

    avg_quality = (
        round(sum(quality_values) / len(quality_values), 1)
        if quality_values
        else 0
    )

    avg_security = (
        round(sum(security_values) / len(security_values), 1)
        if security_values
        else 0
    )

    total_smells = (
        sum(smell_values)
        if smell_values
        else 0
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Total Analyses",
            total_analyses,
        )

    with c2:
        st.metric(
            "Avg Quality",
            f"{avg_quality}/100",
        )

    with c3:
        st.metric(
            "Avg Security",
            f"{avg_security}/100",
        )

    with c4:
        st.metric(
            "Code Smells",
            total_smells,
        )

    st.divider()

    # =====================================================
    # ANALYSIS FEATURES
    # =====================================================

    st.subheader("Analysis Features")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("### 🔍 Code Analysis")

        st.write(
            "Analyze source code and complete projects for "
            "structure, functions, classes and imports."
        )

        st.success("Available")

    with col2:

        st.markdown("### 🛡️ Security Analysis")

        st.write(
            "Detect dangerous functions, suspicious imports, "
            "hardcoded secrets and security risks."
        )

        st.success("Available")

    with col3:

        st.markdown("### 📈 Code Quality")

        st.write(
            "Measure complexity, identify code smells and "
            "evaluate overall project quality."
        )

        st.success("Available")

    st.divider()

    # =====================================================
    # PROJECT INSIGHTS
    # =====================================================

    st.subheader("Project Insights")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 🤖 AI Code Summary")

        st.write(
            "Get an easy-to-understand explanation of your "
            "source code using AI-powered analysis."
        )

    with col2:

        st.markdown("### 🏗️ Project Analysis")

        st.write(
            "Explore project structure, architecture, dependencies, "
            "metrics and code quality."
        )

    st.divider()

    # =====================================================
    # GET STARTED
    # =====================================================

    st.subheader("🚀 Get Started")

    st.info(
        "Use the navigation menu on the left to upload a project "
        "or paste code and start your analysis."
    )

    st.markdown(
        """
        **Recommended workflow**

        1. Open **Analyze Code**
        2. Upload your project or paste source code
        3. Run the available analyses
        4. Review quality and security findings
        5. Check **Analysis History** for saved results
        6. Return to Dashboard to monitor your analysis activity
        """
    )

    st.divider()

    st.caption(
        "CodeInsight AI • Intelligent Static Code Analysis Platform"
    )
