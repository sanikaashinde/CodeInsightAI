import streamlit as st
import os
import sys
from pathlib import Path


def _init_settings():

    defaults = {
        "model": "Gemini",
        "temperature": 0.2,
        "max_response_length": "Balanced",

        "security_enabled": True,
        "complexity_enabled": True,
        "smell_enabled": True,
        "duplicate_enabled": True,
        "dead_code_enabled": True,
        "dependency_enabled": True,
        "todo_enabled": True,
        "documentation_enabled": True,
        "architecture_enabled": True,
        "ai_summary_enabled": True,

        "show_charts": True,
        "show_recommendations": True,
        "auto_expand_findings": False,
        "minimum_severity": "Low",

        "history_limit": 20,
        "auto_save_history": True,

        "max_upload_size": 200,
        "ignore_git": True,
        "ignore_pycache": True,
        "ignore_venv": True,
        "ignore_node_modules": True,

        "privacy_confirm_ai": False,
        "privacy_no_source_storage": True,
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value


def _save_settings(
    model,
    temperature,
    max_response_length,

    security_enabled,
    complexity_enabled,
    smell_enabled,
    duplicate_enabled,
    dead_code_enabled,
    dependency_enabled,
    todo_enabled,
    documentation_enabled,
    architecture_enabled,
    ai_summary_enabled,

    show_charts,
    show_recommendations,
    auto_expand_findings,
    minimum_severity,

    history_limit,
    auto_save_history,

    max_upload_size,
    ignore_git,
    ignore_pycache,
    ignore_venv,
    ignore_node_modules,

    privacy_confirm_ai,
    privacy_no_source_storage,
):

    values = locals()

    for key, value in values.items():
        st.session_state[key] = value


def show_settings():

    _init_settings()

    # =====================================================
    # PAGE HEADER
    # =====================================================

    st.title("⚙️ Settings")

    st.caption(
        "Configure CodeInsight AI analysis, AI behaviour, history, "
        "uploads and privacy preferences."
    )

    st.divider()

    # =====================================================
    # SYSTEM STATUS
    # =====================================================

    st.subheader("System Status")

    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:

        ai_status = "🟢 Connected"
        ai_help = "Gemini API key detected."

    else:

        ai_status = "🟡 Not Configured"
        ai_help = "Gemini API key is not configured. AI features may be unavailable."

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "AI Engine",
            ai_status,
        )

        st.caption(ai_help)

    with c2:

        st.metric(
            "Analysis Engine",
            "🟢 Ready",
        )

    with c3:

        st.metric(
            "Security Scanner",
            "🟢 Enabled"
            if st.session_state.security_enabled
            else "⚪ Disabled",
        )

    with c4:

        st.metric(
            "History",
            "🟢 Active"
            if st.session_state.auto_save_history
            else "⚪ Off",
        )

    st.divider()

    # =====================================================
    # AI CONFIGURATION
    # =====================================================

    st.subheader("🤖 AI Configuration")

    col1, col2 = st.columns(2)

    with col1:

        model = st.selectbox(
            "AI Provider",
            [
                "Gemini",
                "OpenAI",
                "Ollama",
            ],
            index=[
                "Gemini",
                "OpenAI",
                "Ollama",
            ].index(
                st.session_state.model
            ),
        )

    with col2:

        max_response_length = st.selectbox(
            "Response Length",
            [
                "Concise",
                "Balanced",
                "Detailed",
            ],
            index=[
                "Concise",
                "Balanced",
                "Detailed",
            ].index(
                st.session_state.max_response_length
            ),
        )

    temperature = st.slider(
        "Response Creativity",
        min_value=0.0,
        max_value=1.0,
        value=float(
            st.session_state.temperature
        ),
        step=0.1,
        help="Higher values make AI responses more varied.",
    )

    if not api_key and model == "Gemini":

        st.warning(
            "Gemini API is not configured. "
            "Add GEMINI_API_KEY to your .env file to enable AI features."
        )

    st.divider()

    # =====================================================
    # ANALYSIS FEATURES
    # =====================================================

    st.subheader("🔍 Analysis Features")

    st.caption(
        "Choose which static-analysis modules should run on projects."
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        security_enabled = st.toggle(
            "Security Analysis",
            value=st.session_state.security_enabled,
        )

        complexity_enabled = st.toggle(
            "Complexity Analysis",
            value=st.session_state.complexity_enabled,
        )

        smell_enabled = st.toggle(
            "Code Smell Detection",
            value=st.session_state.smell_enabled,
        )

    with c2:

        duplicate_enabled = st.toggle(
            "Duplicate Code",
            value=st.session_state.duplicate_enabled,
        )

        dead_code_enabled = st.toggle(
            "Dead Code",
            value=st.session_state.dead_code_enabled,
        )

        dependency_enabled = st.toggle(
            "Dependency Analysis",
            value=st.session_state.dependency_enabled,
        )

    with c3:

        todo_enabled = st.toggle(
            "TODO Detection",
            value=st.session_state.todo_enabled,
        )

        documentation_enabled = st.toggle(
            "Documentation Analysis",
            value=st.session_state.documentation_enabled,
        )

        architecture_enabled = st.toggle(
            "Architecture Analysis",
            value=st.session_state.architecture_enabled,
        )

    ai_summary_enabled = st.toggle(
        "AI Code Summary",
        value=st.session_state.ai_summary_enabled,
    )

    st.divider()

    # =====================================================
    # OUTPUT PREFERENCES
    # =====================================================

    st.subheader("📊 Analysis Output")

    col1, col2 = st.columns(2)

    with col1:

        show_charts = st.toggle(
            "Show Charts & Visualizations",
            value=st.session_state.show_charts,
        )

        show_recommendations = st.toggle(
            "Show Recommendations",
            value=st.session_state.show_recommendations,
        )

    with col2:

        auto_expand_findings = st.toggle(
            "Auto-expand Important Findings",
            value=st.session_state.auto_expand_findings,
        )

        minimum_severity = st.selectbox(
            "Minimum Finding Severity",
            [
                "Low",
                "Medium",
                "High",
                "Critical",
            ],
            index=[
                "Low",
                "Medium",
                "High",
                "Critical",
            ].index(
                st.session_state.minimum_severity
            ),
        )

    st.divider()

    # =====================================================
    # HISTORY
    # =====================================================

    st.subheader("🕘 History & Storage")

    col1, col2 = st.columns(2)

    with col1:

        history_limit = st.slider(
            "Maximum History Records",
            min_value=5,
            max_value=50,
            value=int(
                st.session_state.history_limit
            ),
            step=5,
        )

    with col2:

        auto_save_history = st.toggle(
            "Automatically Save Analysis History",
            value=st.session_state.auto_save_history,
        )

    st.caption(
        f"Up to {history_limit} recent analysis records will be retained."
    )

    st.divider()

    # =====================================================
    # UPLOAD / PROJECT SETTINGS
    # =====================================================

    st.subheader("📁 Project & Upload Preferences")

    max_upload_size = st.slider(
        "Maximum Upload Size (MB)",
        min_value=50,
        max_value=1000,
        value=int(
            st.session_state.max_upload_size
        ),
        step=50,
    )

    st.caption(
        "Larger projects may require more memory and processing time."
    )

    st.markdown("**Ignore During Project Scan**")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        ignore_git = st.checkbox(
            "Ignore .git",
            value=st.session_state.ignore_git,
        )

    with c2:

        ignore_pycache = st.checkbox(
            "Ignore __pycache__",
            value=st.session_state.ignore_pycache,
        )

    with c3:

        ignore_venv = st.checkbox(
            "Ignore venv",
            value=st.session_state.ignore_venv,
        )

    with c4:

        ignore_node_modules = st.checkbox(
            "Ignore node_modules",
            value=st.session_state.ignore_node_modules,
        )

    st.divider()

    # =====================================================
    # PRIVACY
    # =====================================================

    st.subheader("🔐 Privacy & Security")

    privacy_confirm_ai = st.toggle(
        "Ask Before Sending Code to AI",
        value=st.session_state.privacy_confirm_ai,
        help="Ask for confirmation before AI-powered analysis.",
    )

    privacy_no_source_storage = st.toggle(
        "Don't Store Uploaded Source Code",
        value=st.session_state.privacy_no_source_storage,
        help="Prefer temporary processing instead of retaining source files.",
    )

    st.divider()

    # =====================================================
    # SAVE / RESET
    # =====================================================

    st.subheader("💾 Settings Management")

    save_col, reset_col = st.columns(2)

    with save_col:

        if st.button(
            "💾 Save Settings",
            type="primary",
            use_container_width=True,
        ):

            _save_settings(
                model,
                temperature,
                max_response_length,

                security_enabled,
                complexity_enabled,
                smell_enabled,
                duplicate_enabled,
                dead_code_enabled,
                dependency_enabled,
                todo_enabled,
                documentation_enabled,
                architecture_enabled,
                ai_summary_enabled,

                show_charts,
                show_recommendations,
                auto_expand_findings,
                minimum_severity,

                history_limit,
                auto_save_history,

                max_upload_size,
                ignore_git,
                ignore_pycache,
                ignore_venv,
                ignore_node_modules,

                privacy_confirm_ai,
                privacy_no_source_storage,
            )

            st.success(
                "Settings saved successfully."
            )

    with reset_col:

        if st.button(
            "↩️ Restore Defaults",
            use_container_width=True,
        ):

            keys = [
                "model",
                "temperature",
                "max_response_length",

                "security_enabled",
                "complexity_enabled",
                "smell_enabled",
                "duplicate_enabled",
                "dead_code_enabled",
                "dependency_enabled",
                "todo_enabled",
                "documentation_enabled",
                "architecture_enabled",
                "ai_summary_enabled",

                "show_charts",
                "show_recommendations",
                "auto_expand_findings",
                "minimum_severity",

                "history_limit",
                "auto_save_history",

                "max_upload_size",
                "ignore_git",
                "ignore_pycache",
                "ignore_venv",
                "ignore_node_modules",

                "privacy_confirm_ai",
                "privacy_no_source_storage",
            ]

            for key in keys:
                if key in st.session_state:
                    del st.session_state[key]

            st.success(
                "Default settings restored."
            )

            st.rerun()

    st.divider()

    # =====================================================
    # CURRENT CONFIGURATION
    # =====================================================

    st.subheader("📋 Current Configuration")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.write(
            f"**AI Provider:** "
            f"{st.session_state.model}"
        )

        st.write(
            f"**Response Style:** "
            f"{st.session_state.max_response_length}"
        )

    with c2:

        st.write(
            f"**Temperature:** "
            f"{st.session_state.temperature}"
        )

        st.write(
            f"**History Limit:** "
            f"{st.session_state.history_limit}"
        )

    with c3:

        enabled_count = sum(
            [
                st.session_state.security_enabled,
                st.session_state.complexity_enabled,
                st.session_state.smell_enabled,
                st.session_state.duplicate_enabled,
                st.session_state.dead_code_enabled,
                st.session_state.dependency_enabled,
                st.session_state.todo_enabled,
                st.session_state.documentation_enabled,
                st.session_state.architecture_enabled,
            ]
        )

        st.write(
            f"**Analysis Modules:** "
            f"{enabled_count}/9 enabled"
        )

        st.write(
            f"**Upload Limit:** "
            f"{st.session_state.max_upload_size} MB"
        )

    st.divider()

    # =====================================================
    # DANGER ZONE
    # =====================================================

    st.subheader("⚠️ Data Management")

    if st.button(
        "🗑️ Clear Analysis History",
        use_container_width=True,
    ):

        st.session_state.analysis_history = []

        st.success(
            "Analysis history cleared successfully."
        )

    st.caption(
        "CodeInsight AI • Settings are maintained for the current session."
    )

