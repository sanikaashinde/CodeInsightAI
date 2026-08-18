import streamlit as st

from core.auth import (
    register_user,
    login_user,
)


def show_auth_page():

    st.markdown(
        """
        <style>
        .auth-container {
            max-width: 520px;
            margin: 50px auto;
        }

        .auth-title {
            text-align: center;
            font-size: 42px;
            font-weight: 800;
            margin-bottom: 5px;
        }

        .auth-subtitle {
            text-align: center;
            color: #7b8190;
            margin-bottom: 30px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="auth-container">',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="auth-title">💻 CodeInsight AI</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="auth-subtitle">Intelligent Code Analysis Platform</div>',
        unsafe_allow_html=True,
    )

    login_tab, register_tab = st.tabs(
        ["🔐 Login", "📝 Register"]
    )

    # =====================================================
    # LOGIN
    # =====================================================

    with login_tab:

        st.subheader("Welcome Back 👋")

        identifier = st.text_input(
            "Email or Username",
            placeholder="Enter your email or username",
            key="login_identifier",
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password",
        )

        remember = st.checkbox(
            "Remember me",
            key="remember_me",
        )

        if st.button(
            "🔐 Login",
            use_container_width=True,
            type="primary",
        ):

            if not identifier or not password:
                st.error("Please enter both username/email and password.")

            else:

                user = login_user(
                    identifier,
                    password,
                )

                if user:

                    st.session_state.authenticated = True
                    st.session_state.user = user

                    if remember:
                        st.session_state.remember_me = True

                    st.success(
                        f"Welcome back, {user['full_name']}!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Invalid username/email or password."
                    )

    # =====================================================
    # REGISTER
    # =====================================================

    with register_tab:

        st.subheader("Create Your Account")

        full_name = st.text_input(
            "Full Name",
            placeholder="Enter your full name",
            key="register_name",
        )

        email = st.text_input(
            "Email",
            placeholder="example@gmail.com",
            key="register_email",
        )

        username = st.text_input(
            "Username",
            placeholder="Choose a username",
            key="register_username",
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a strong password",
            key="register_password",
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password",
            key="register_confirm_password",
        )

        if password:

            if len(password) < 8:
                st.warning(
                    "Password should contain at least 8 characters."
                )

            elif (
                any(c.isupper() for c in password)
                and any(c.islower() for c in password)
                and any(c.isdigit() for c in password)
            ):
                st.success("Strong password ✓")

            else:
                st.info(
                    "Use uppercase, lowercase and numbers for a stronger password."
                )

        terms = st.checkbox(
            "I agree to the Terms & Conditions",
            key="terms",
        )

        if st.button(
            "📝 Create Account",
            use_container_width=True,
            type="primary",
        ):

            if not full_name:
                st.error("Please enter your full name.")

            elif not email or "@" not in email:
                st.error("Please enter a valid email.")

            elif not username:
                st.error("Please choose a username.")

            elif len(password) < 8:
                st.error(
                    "Password must contain at least 8 characters."
                )

            elif password != confirm_password:
                st.error("Passwords do not match.")

            elif not terms:
                st.error(
                    "Please accept the Terms & Conditions."
                )

            else:

                success, message = register_user(
                    full_name,
                    email,
                    username,
                    password,
                )

                if success:

                    st.success(message)

                    st.info(
                        "Your account has been created. "
                        "Please open the Login tab and sign in."
                    )

                else:

                    st.error(message)

    st.markdown("</div>", unsafe_allow_html=True)
