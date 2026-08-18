import streamlit as st

from core.auth import init_auth_db
from app.auth_page import show_auth_page

from app.pages.dashboard import show_dashboard
from app.pages.analyze import show_analyze
from app.pages.history import show_history
from app.pages.settings import show_settings


# =========================================================
# DATABASE
# =========================================================

init_auth_db()


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="CodeInsight AI",
    page_icon="C",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# SESSION STATE
# =========================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user" not in st.session_state:
    st.session_state.user = None


# =========================================================
# GLOBAL DESIGN
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       GLOBAL
       ===================================================== */

    .stApp {
        background: #f7f8fc;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1 {
        font-size: 2.25rem !important;
        font-weight: 750 !important;
        letter-spacing: -0.7px;
        color: #111827;
    }

    h2 {
        font-size: 1.65rem !important;
        font-weight: 700 !important;
        color: #111827;
    }

    h3 {
        font-size: 1.25rem !important;
        font-weight: 650 !important;
        color: #111827;
    }

    p {
        color: #667085;
    }



    /* =====================================================
       TEXT VISIBILITY FIX
       ===================================================== */

    .stApp,
    .stApp p,
    .stApp label,
    .stApp span,
    .stApp div {
        color: #1d2939;
    }

    .stMarkdown,
    .stMarkdown p {
        color: #344054;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #101828 !important;
    }

    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] * {
        color: #344054;
    }

    section[data-testid="stSidebar"] .brand-title {
        color: #101828 !important;
    }

    section[data-testid="stSidebar"] .brand-subtitle {
        color: #667085 !important;
    }

    section[data-testid="stSidebar"] .profile-name {
        color: #344054 !important;
    }

    section[data-testid="stSidebar"] .profile-email {
        color: #667085 !important;
    }

    section[data-testid="stSidebar"] .nav-label {
        color: #667085 !important;
    }

    div[role="radiogroup"] label p {
        color: #344054 !important;
    }

    .stButton > button {
        color: #344054 !important;
        background-color: #ffffff !important;
    }

    .stTextInput label,
    .stTextArea label,
    .stSelectbox label,
    .stRadio label {
        color: #344054 !important;
    }

    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input {
        color: #101828 !important;
        background-color: #ffffff !important;
    }

    div[data-testid="stMetricLabel"] {
        color: #667085 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #101828 !important;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e7e9ef;
    }

    section[data-testid="stSidebar"] > div {
        padding: 1.2rem 0.9rem;
    }


    /* Brand */

    .brand-box {
        padding: 12px 12px 22px 12px;
    }

    .brand-title {
        font-size: 21px;
        font-weight: 800;
        color: #111827;
        letter-spacing: -0.4px;
    }

    .brand-subtitle {
        font-size: 11px;
        color: #98a2b3;
        margin-top: 4px;
    }


    /* User */

    .profile-card {
        background: #f8f9fc;
        border: 1px solid #eaecf0;
        border-radius: 12px;
        padding: 12px;
        margin: 5px 4px 20px 4px;
    }

    .profile-name {
        font-size: 13px;
        font-weight: 700;
        color: #344054;
    }

    .profile-email {
        font-size: 10px;
        color: #98a2b3;
        margin-top: 3px;
        word-break: break-word;
    }


    /* Navigation label */

    .nav-label {
        font-size: 10px;
        font-weight: 750;
        color: #98a2b3;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin: 10px 8px 8px 8px;
    }


    /* Radio navigation */

    div[role="radiogroup"] {
        gap: 4px;
    }

    div[role="radiogroup"] label {
        border-radius: 9px;
        padding: 9px 10px;
        margin: 1px 0;
        border: 1px solid transparent;
        transition: all 0.15s ease;
    }

    div[role="radiogroup"] label:hover {
        background: #f3f4f7;
    }

    div[role="radiogroup"] label p {
        font-size: 13px;
        font-weight: 550;
        color: #475467;
    }


    /* Logout */

    .logout-divider {
        height: 1px;
        background: #eaecf0;
        margin: 18px 4px 12px 4px;
    }


    /* =====================================================
       BUTTONS
       ===================================================== */

    .stButton > button {
        border-radius: 9px;
        min-height: 40px;
        font-weight: 600;
        border: 1px solid #d0d5dd;
        transition: all 0.15s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        border-color: #98a2b3;
    }


    /* =====================================================
       CARDS / METRICS
       ===================================================== */

    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #eaecf0;
        border-radius: 13px;
        padding: 17px;
        box-shadow: 0 1px 2px rgba(16,24,40,0.03);
    }

    div[data-testid="stMetricLabel"] {
        color: #667085;
        font-size: 12px;
    }

    div[data-testid="stMetricValue"] {
        color: #101828;
        font-weight: 750;
    }


    /* =====================================================
       INPUTS
       ===================================================== */

    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input {
        border-radius: 9px !important;
        border: 1px solid #d0d5dd !important;
    }


    /* =====================================================
       CONTAINERS
       ===================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 13px;
        border-color: #eaecf0;
    }


    /* =====================================================
       DATAFRAME
       ===================================================== */

    div[data-testid="stDataFrame"] {
        border-radius: 11px;
        overflow: hidden;
        border: 1px solid #eaecf0;
    }


    /* =====================================================
       ALERTS
       ===================================================== */

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }


    /* =====================================================
       EXPANDERS
       ===================================================== */

    details {
        border-radius: 11px !important;
        border: 1px solid #eaecf0 !important;
        background: #ffffff;
    }


    /* =====================================================
       FOOTER
       ===================================================== */

    .sidebar-footer {
        margin: 20px 4px 0 4px;
        padding: 13px 4px;
        border-top: 1px solid #eaecf0;
        color: #98a2b3;
        font-size: 10px;
        line-height: 1.5;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# LOGIN GATE
# =========================================================

if not st.session_state.authenticated:

    show_auth_page()

    st.stop()


# =========================================================
# LOGGED-IN USER
# =========================================================

user = st.session_state.user


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    # -----------------------------------------------------
    # BRAND
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="brand-box">
            <div class="brand-title">
                CodeInsight AI
            </div>

            <div class="brand-subtitle">
                Intelligent Code Analysis Platform
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


    # -----------------------------------------------------
    # PROFILE
    # -----------------------------------------------------

    st.markdown(
        f"""
        <div class="profile-card">

            <div class="profile-name">
                {user["full_name"]}
            </div>

            <div class="profile-email">
                {user["email"]}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # -----------------------------------------------------
    # NAVIGATION
    # -----------------------------------------------------

    st.markdown(
        '<div class="nav-label">Workspace</div>',
        unsafe_allow_html=True,
    )


    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Analyze Code",
            "Analysis History",
            "Settings",
        ],
        label_visibility="collapsed",
    )


    # -----------------------------------------------------
    # LOGOUT
    # -----------------------------------------------------

    st.markdown(
        '<div class="logout-divider"></div>',
        unsafe_allow_html=True,
    )


    if st.button(
        "Logout",
        use_container_width=True,
    ):

        st.session_state.authenticated = False
        st.session_state.user = None

        st.rerun()


    # -----------------------------------------------------
    # FOOTER
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="sidebar-footer">
            CodeInsight AI<br>
            Intelligent static code analysis<br>
            Version 2.0
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# PAGE ROUTING
# =========================================================

if page == "Dashboard":

    show_dashboard()


elif page == "Analyze Code":

    show_analyze()


elif page == "Analysis History":

    show_history()


elif page == "Settings":

    show_settings()
