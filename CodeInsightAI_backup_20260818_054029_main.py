import streamlit as st

from core.auth import init_auth_db
from app.auth_page import show_auth_page

from app.pages.dashboard import show_dashboard
from app.pages.analyze import show_analyze
from app.pages.history import show_history
from app.pages.settings import show_settings


# =========================================================
# INITIALIZATION
# =========================================================

init_auth_db()

st.set_page_config(
    page_title="CodeInsight AI",
    page_icon="CI",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# SESSION
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

.stApp {
    background: #f6f8fb;
}

.block-container {
    max-width: 1500px;
    padding: 28px 38px 50px 38px;
}

h1, h2, h3, h4, h5, h6 {
    color: #101828 !important;
}

p, label {
    color: #475467;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {
    background: #111827 !important;
    border-right: 1px solid #1f2937 !important;
}

section[data-testid="stSidebar"] > div {
    background: #111827 !important;
    padding: 18px 14px 20px 14px !important;
}


/* Brand */

.sidebar-brand {
    padding: 8px 8px 22px 8px;
}

.sidebar-brand-row {
    display: flex;
    align-items: center;
    gap: 10px;
}

.sidebar-brand-mark {
    width: 36px;
    height: 36px;
    min-width: 36px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: #ffffff;
    color: #111827 !important;

    border-radius: 10px;

    font-size: 14px;
    font-weight: 800;
}

.sidebar-brand-title {
    color: #ffffff !important;
    font-size: 19px;
    font-weight: 750;
    white-space: nowrap;
}

.sidebar-brand-subtitle {
    color: #98a2b3 !important;
    font-size: 11px;
    margin-top: 7px;
    margin-left: 46px;
}


/* User Card */

.sidebar-user {
    background: #1d2939;
    border: 1px solid #344054;
    border-radius: 12px;

    padding: 13px 14px;
    margin: 0 3px 24px 3px;

    overflow: hidden;
}

.sidebar-user-label {
    color: #98a2b3 !important;
    font-size: 9px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.sidebar-user-name {
    color: #ffffff !important;
    font-size: 14px;
    font-weight: 700;
    margin-top: 6px;
}

.sidebar-user-email {
    color: #98a2b3 !important;
    font-size: 10px;
    margin-top: 4px;
    line-height: 1.4;

    overflow-wrap: anywhere;
    word-break: break-word;
}


/* Workspace */

.sidebar-section {
    color: #667085 !important;
    font-size: 9px;
    font-weight: 800;

    text-transform: uppercase;
    letter-spacing: 1.2px;

    padding: 0 9px 8px 9px;
}


/* Navigation */

div[role="radiogroup"] {
    gap: 4px !important;
}

div[role="radiogroup"] label {
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 9px !important;

    padding: 9px 10px !important;
    margin: 1px 0 !important;
}

div[role="radiogroup"] label:hover {
    background: #1d2939 !important;
    border-color: #344054 !important;
}

div[role="radiogroup"] label p {
    color: #d0d5dd !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}


/* Footer */

.sidebar-footer {
    margin: 22px 5px 0 5px;
    padding: 14px 8px;

    border-top: 1px solid #344054;

    color: #667085 !important;
    font-size: 10px;
    line-height: 1.7;
}


/* Logout */

section[data-testid="stSidebar"] .stButton {
    margin-top: 14px;
}

section[data-testid="stSidebar"] .stButton > button {
    background: #1d2939 !important;
    color: #d0d5dd !important;

    border: 1px solid #344054 !important;
    border-radius: 9px !important;

    min-height: 38px !important;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: #344054 !important;
    color: #ffffff !important;
}


/* =========================================================
   TOP HEADER
   ========================================================= */

.top-header {
    width: 100%;
    min-height: 62px;

    display: flex;
    align-items: center;
    justify-content: space-between;

    background: #ffffff;

    border: 1px solid #eaecf0;
    border-radius: 13px;

    padding: 12px 18px;
    margin-bottom: 24px;

    box-shadow: 0 2px 8px rgba(16,24,40,0.035);

    box-sizing: border-box;
}

.top-header-left {
    min-width: 0;
}

.top-header-title {
    color: #101828 !important;
    font-size: 14px;
    font-weight: 750;
}

.top-header-subtitle {
    color: #98a2b3 !important;
    font-size: 10px;
    margin-top: 3px;
}

.top-user {
    color: #344054 !important;

    background: #f2f4f7;
    border: 1px solid #eaecf0;

    border-radius: 8px;

    padding: 7px 12px;

    font-size: 11px;
    font-weight: 700;

    white-space: nowrap;
}


/* =========================================================
   MAIN CARDS
   ========================================================= */

div[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid #eaecf0 !important;
    border-radius: 13px !important;

    padding: 17px !important;

    box-shadow: 0 2px 7px rgba(16,24,40,0.035);
}

div[data-testid="stMetricLabel"] {
    color: #667085 !important;
}

div[data-testid="stMetricValue"] {
    color: #101828 !important;
    font-weight: 800 !important;
}


/* Buttons */

.stButton > button {
    min-height: 40px;

    border-radius: 9px !important;

    border: 1px solid #d0d5dd !important;
    background: #ffffff !important;

    color: #344054 !important;

    font-weight: 650 !important;
}


/* Inputs */

.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background: #ffffff !important;
    color: #101828 !important;

    border: 1px solid #d0d5dd !important;
    border-radius: 9px !important;
}

.stTextInput label,
.stTextArea label,
.stNumberInput label {
    color: #344054 !important;
    font-weight: 600 !important;
}


/* Containers */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #ffffff;
    border: 1px solid #eaecf0;
    border-radius: 13px;
}


/* Expanders */

details {
    background: #ffffff !important;
    border: 1px solid #eaecf0 !important;
    border-radius: 11px !important;
}


/* Alerts */

div[data-testid="stAlert"] {
    border-radius: 9px !important;
}


/* Divider */

hr {
    border-color: #eaecf0 !important;
}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 900px) {

    .block-container {
        padding: 20px 18px 40px 18px;
    }

    .top-header {
        padding: 11px 14px;
    }

}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# AUTHENTICATION
# =========================================================

if not st.session_state.authenticated:

    show_auth_page()

    st.stop()


# =========================================================
# CURRENT USER
# =========================================================

user = st.session_state.user


# =========================================================
# TOP HEADER
# =========================================================

st.html(
    f"""
    <div class="top-header">

        <div class="top-header-left">

            <div class="top-header-title">
                CodeInsight AI Workspace
            </div>

            <div class="top-header-subtitle">
                Intelligent static code analysis platform
            </div>

        </div>

        <div class="top-user">
            {user["full_name"]}
        </div>

    </div>
    """
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    # BRAND
    st.html(
        """
        <div class="sidebar-brand">

            <div class="sidebar-brand-row">

                <span class="sidebar-brand-mark">
                    CI
                </span>

                <span class="sidebar-brand-title">
                    CodeInsight AI
                </span>

            </div>

            <div class="sidebar-brand-subtitle">
                Intelligent Code Analysis
            </div>

        </div>
        """
    )


    # USER
    st.html(
        f"""
        <div class="sidebar-user">

            <div class="sidebar-user-label">
                Signed in as
            </div>

            <div class="sidebar-user-name">
                {user["full_name"]}
            </div>

            <div class="sidebar-user-email">
                {user["email"]}
            </div>

        </div>
        """
    )


    # WORKSPACE
    st.markdown(
        '<div class="sidebar-section">Workspace</div>',
        unsafe_allow_html=True,
    )


    # NAVIGATION
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


    # FOOTER
    st.html(
        """
        <div class="sidebar-footer">
            <strong>CodeInsight AI</strong><br>
            Static analysis workspace<br>
            Version 2.0
        </div>
        """
    )


    # LOGOUT
    if st.button(
        "Logout",
        use_container_width=True,
    ):

        st.session_state.authenticated = False
        st.session_state.user = None

        st.rerun()


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
