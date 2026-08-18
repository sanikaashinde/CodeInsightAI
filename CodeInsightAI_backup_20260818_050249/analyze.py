import streamlit as st

from app.pages.upload import show_upload
from app.pages.paste import show_paste


def show_analyze():

    # ==========================================
    # PAGE HEADER
    # ==========================================

    st.title(" Analyze Code")

    st.caption(
        "Analyze your source code or complete project using "
        "CodeInsight AI's intelligent static analysis engine."
    )

    st.divider()

    # ==========================================
    # ANALYSIS FEATURES
    # ==========================================

    st.subheader("Analysis Features")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.info(
            " Security\n\n"
            "Detect dangerous functions, imports, "
            "hardcoded secrets and security risks."
        )

    with col2:
        st.info(
            " Complexity\n\n"
            "Measure code complexity and identify "
            "difficult functions."
        )

    with col3:
        st.info(
            " Code Smells\n\n"
            "Find maintainability issues and "
            "problematic coding patterns."
        )

    with col4:
        st.info(
            " AI Summary\n\n"
            "Generate an AI-powered explanation "
            "of your code."
        )

    st.divider()

    # ==========================================
    # INPUT METHOD
    # ==========================================

    st.subheader("Choose Analysis Source")

    st.caption(
        "Select how you want to provide your code."
    )

    input_method = st.radio(
        "Analysis source",
        [
            " Upload Project",
            " Paste Code",
        ],
        horizontal=True,
        key="analyze_input_method",
        label_visibility="collapsed",
    )

    st.divider()

    # ==========================================
    # UPLOAD PROJECT
    # ==========================================

    if input_method == " Upload Project":

        st.subheader(" Upload Project")

        st.caption(
            "Upload a ZIP project or source files "
            "to start complete analysis."
        )

        show_upload()

    # ==========================================
    # PASTE CODE
    # ==========================================

    else:

        st.subheader(" Paste Code")

        st.caption(
            "Paste Python code below to run static analysis."
        )

        show_paste()

