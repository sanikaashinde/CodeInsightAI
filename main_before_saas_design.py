import streamlit as st

from core.auth import init_auth_db
from app.auth_page import show_auth_page

from app.pages.dashboard import show_dashboard
from app.pages.analyze import show_analyze
from app.pages.history import show_history
from app.pages.settings import show_settings


# =========================================================
# INITIALIZE DATABASE
# =========================================================

init_auth_db()


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
# SESSION STATE
# =========================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user" not in st.session_state:
    st.session_state.user = None


# =========================================================
# GLOBAL UI
# =========================================================

st.markdown(
    """
    <style>

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

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

    .stButton > button {
        border-radius: 9px;
        font-weight: 600;
        min-height: 40px;
        transition: all 0.18s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
    }

    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input {
        border-radius: 9px !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 13px;
    }

    details {
        border-radius: 11px !important;
        border: 1px solid rgba(128,128,128,0.18) !important;
    }

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
    }

    pre {
        border-radius: 10px !important;
    }

    button[data-baseweb="tab"] {
        font-weight: 600;
    }

    .sidebar-footer {
        margin-top: 25px;
        padding: 12px 8px;
        border-top: 1px solid rgba(128,128,128,0.16);
        color: #8b91a0;
        font-size: 11px;
        line-height: 1.5;
    }

    .user-card {
        padding: 12px;
        margin: 5px 0 15px 0;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.18);
        background: rgba(128,128,128,0.04);
    }

    .user-name {
        font-size: 14px;
        font-weight: 700;
    }

    .user-email {
        font-size: 11px;
        color: #7b8190;
        margin-top: 3px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# AUTHENTICATION GATE
# =========================================================

if not st.session_state.authenticated:

    show_auth_page()

    st.stop()


# =========================================================
# CURRENT USER
# =========================================================

user = st.session_state.user


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        "## CodeInsight AI"
    )

    st.caption(
        "Code Analysis Platform"
    )

    # -----------------------------------------------------
    # USER INFO
    # -----------------------------------------------------

    st.markdown(
        f"**User: {user['full_name']}**"
    )

    st.caption(
        user["email"]
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

    st.divider()

    # -----------------------------------------------------
    # LOGOUT
    # -----------------------------------------------------

    if st.button(
        "🚪 Logout",
        use_container_width=True,
    ):

        st.session_state.authenticated = False
        st.session_state.user = None

        st.rerun()

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
