import streamlit as st

from app.pages.upload import show_upload
from app.pages.paste import show_paste


def show_analyze():

    # =========================================================
    # PAGE HEADER
    # =========================================================

    st.markdown(
        """
    

            <div style="
                margin-top: 6px;
                font-size: 14px;
                color: #667085;
            ">
                Analyze source code or complete projects using
                intelligent static analysis.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # =========================================================
    # ANALYSIS CAPABILITIES
    # =========================================================

    st.markdown(
        """
        <div style="
            font-size: 18px;
            font-weight: 750;
            color: #101828;
            margin-bottom: 14px;
        ">
            Analysis Capabilities
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            """
            <div style="
                background:#ffffff;
                border:1px solid #eaecf0;
                border-radius:14px;
                padding:18px;
                min-height:120px;
            ">
                <div style="font-size:22px;">Security</div>
                <div style="
                    margin-top:8px;
                    font-size:12px;
                    color:#667085;
                    line-height:1.5;
                ">
                    Detect dangerous functions, imports,
                    secrets and security risks.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div style="
                background:#ffffff;
                border:1px solid #eaecf0;
                border-radius:14px;
                padding:18px;
                min-height:120px;
            ">
                <div style="font-size:22px;">Complexity</div>
                <div style="
                    margin-top:8px;
                    font-size:12px;
                    color:#667085;
                    line-height:1.5;
                ">
                    Measure cyclomatic complexity
                    and identify difficult functions.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            """
            <div style="
                background:#ffffff;
                border:1px solid #eaecf0;
                border-radius:14px;
                padding:18px;
                min-height:120px;
            ">
                <div style="font-size:22px;">Code Quality</div>
                <div style="
                    margin-top:8px;
                    font-size:12px;
                    color:#667085;
                    line-height:1.5;
                ">
                    Find code smells and evaluate
                    maintainability.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            """
            <div style="
                background:#ffffff;
                border:1px solid #eaecf0;
                border-radius:14px;
                padding:18px;
                min-height:120px;
            ">
                <div style="font-size:22px;">AI Summary</div>
                <div style="
                    margin-top:8px;
                    font-size:12px;
                    color:#667085;
                    line-height:1.5;
                ">
                    Generate an AI-powered explanation
                    of your code.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================================================
    # SOURCE SELECTION
    # =========================================================

    st.markdown(
        """
        <div style="
            font-size:18px;
            font-weight:750;
            color:#101828;
            margin-bottom:4px;
        ">
            Choose Analysis Source
        </div>

        <div style="
            font-size:12px;
            color:#667085;
            margin-bottom:12px;
        ">
            Select how you want to provide your code.
        </div>
        """,
        unsafe_allow_html=True,
    )

    input_method = st.radio(
        "Analysis source",
        [
            "Upload Project",
            "Paste Code",
        ],
        horizontal=True,
        key="analyze_input_method",
        label_visibility="collapsed",
    )

    st.divider()

    # =========================================================
    # UPLOAD PROJECT
    # =========================================================

    if input_method == "Upload Project":

        show_upload()

    # =========================================================
    # PASTE CODE
    # =========================================================

    else:

        show_paste()
