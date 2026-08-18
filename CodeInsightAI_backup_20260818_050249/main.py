import streamlit as st

from app.pages.dashboard import show_dashboard
from app.pages.analyze import show_analyze
from app.pages.history import show_history
from app.pages.settings import show_settings


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="CodeInsight AI",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# GLOBAL UI
# =========================================================

st.markdown(
    """
    <style>

    /* ---------- Main Layout ---------- */

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* ---------- Typography ---------- */

    h1 {
        font-size: 2.35rem !important;
        font-weight: 750 !important;
        letter-spacing: -0.7px;
    }

    h2 {
        font-size: 1.75rem !important;
        font-weight: 700 !important;
    }

    h3 {
        font-size: 1.3rem !important;
        font-weight: 650 !important;
    }

    /* ---------- Sidebar ---------- */

    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(128,128,128,0.18);
    }

    section[data-testid="stSidebar"] > div {
        padding: 1.4rem 1rem 1rem 1rem;
    }

    .sidebar-brand {
        padding: 8px 8px 16px 8px;
    }

    .sidebar-logo {
        font-size: 25px;
        font-weight: 750;
        letter-spacing: -0.5px;
    }

    .sidebar-tagline {
        color: #7b8190;
        font-size: 12px;
        margin-top: 3px;
    }

    .sidebar-section {
        font-size: 11px;
        font-weight: 700;
        color: #8b91a0;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        padding: 8px 8px 5px 8px;
    }

    /* ---------- Navigation ---------- */

    div[role="radiogroup"] {
        gap: 5px;
    }

    div[role="radiogroup"] label {
        border-radius: 10px;
        padding: 9px 10px;
        margin: 2px 0;
        transition: all 0.18s ease;
    }

    div[role="radiogroup"] label:hover {
        background: rgba(128,128,128,0.09);
    }

    div[role="radiogroup"] label p {
        font-size: 14px;
        font-weight: 550;
    }

    /* ---------- Metrics ---------- */

    div[data-testid="stMetric"] {
        border: 1px solid rgba(128,128,128,0.18);
        border-radius: 13px;
        padding: 16px;
        background: rgba(128,128,128,0.035);
    }

    div[data-testid="stMetricLabel"] {
        font-size: 0.82rem;
    }

    div[data-testid="stMetricValue"] {
        font-weight: 750;
    }

    /* ---------- Buttons ---------- */

    .stButton > button {
        border-radius: 9px;
        font-weight: 600;
        min-height: 40px;
        transition: all 0.18s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
    }

    /* ---------- Inputs ---------- */

    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input {
        border-radius: 9px !important;
    }

    /* ---------- Containers ---------- */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 13px;
    }

    /* ---------- Expanders ---------- */

    details {
        border-radius: 11px !important;
        border: 1px solid rgba(128,128,128,0.18) !important;
    }

    /* ---------- Alerts ---------- */

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

    /* ---------- Dataframes ---------- */

    div[data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
    }

    /* ---------- Code Blocks ---------- */

    pre {
        border-radius: 10px !important;
    }

    /* ---------- Tabs ---------- */

    button[data-baseweb="tab"] {
        font-weight: 600;
    }

    /* ---------- Footer ---------- */

    .sidebar-footer {
        margin-top: 25px;
        padding: 12px 8px;
        border-top: 1px solid rgba(128,128,128,0.16);
        color: #8b91a0;
        font-size: 11px;
        line-height: 1.5;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-logo">💻 CodeInsight AI</div>
            <div class="sidebar-tagline">
                Intelligent Code Analysis Platform
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-section">Workspace</div>',
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        [
            "🏠  Dashboard",
            "🔍  Analyze Code",
            "📊  Analysis History",
            "⚙️  Settings",
        ],
        label_visibility="collapsed",
    )

    st.markdown(
        """
        <div class="sidebar-footer">
            <strong>CodeInsight AI</strong><br>
            Intelligent static code analysis<br>
            <span>Version 2.0</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# ROUTING
# =========================================================

if page == "🏠  Dashboard":

    show_dashboard()


elif page == "🔍  Analyze Code":

    show_analyze()


elif page == "📊  Analysis History":

    show_history()


elif page == "⚙️  Settings":

    show_settings()
