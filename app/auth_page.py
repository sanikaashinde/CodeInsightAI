import streamlit as st

from core.auth import (
    register_user,
    login_user,
)


def show_auth_page():

    # =====================================================
    # AUTH PAGE CSS
    # =====================================================

    st.markdown(
        """
        <style>

        .auth-title-text {
            text-align: center;
            font-size: 30px;
            font-weight: 800;
            color: #101828;
            letter-spacing: -0.8px;
            margin-top: 15px;
        }

        .auth-subtitle-text {
            text-align: center;
            color: #667085;
            font-size: 13px;
            margin-top: 5px;
            margin-bottom: 25px;
        }

        .auth-logo-box {
            width: 58px;
            height: 58px;
            border-radius: 16px;
            background: #101828;
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            font-weight: 800;
            margin: 0 auto 14px auto;
            box-shadow: 0 8px 25px rgba(16,24,40,0.15);
        }

        .auth-footer-text {
            text-align: center;
            color: #98A2B3;
            font-size: 11px;
            margin-top: 20px;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


    # =====================================================
    # CENTERED BRAND
    # =====================================================

    left, center, right = st.columns([1, 2, 1])

    with center:

        st.html(
            """
            <div style="
                text-align:center;
                padding-top:20px;
            ">

                <div class="auth-logo-box">
                    CI
                </div>

                <div class="auth-title-text">
                    CodeInsight AI
                </div>

                <div class="auth-subtitle-text">
                    Intelligent static code analysis platform
                </div>

            </div>
            """
        )


        # =================================================
        # AUTH CARD
        # =================================================

        login_tab, register_tab = st.tabs(
            ["Login", "Create Account"]
        )


        # =================================================
        # LOGIN
        # =================================================

        with login_tab:

            st.html(
                """
                <div style="
                    margin-top:12px;
                    margin-bottom:18px;
                ">

                    <div style="
                        color:#101828;
                        font-size:21px;
                        font-weight:750;
                    ">
                        Welcome back
                    </div>

                    <div style="
                        color:#667085;
                        font-size:12px;
                        margin-top:5px;
                    ">
                        Sign in to continue to your workspace.
                    </div>

                </div>
                """
            )


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
                "Sign in",
                use_container_width=True,
                type="primary",
                key="login_button",
            ):

                if not identifier or not password:

                    st.error(
                        "Please enter both username/email and password."
                    )

                else:

                    user = login_user(
                        identifier,
                        password,
                    )

                    if user:

                        st.session_state.authenticated = True
                        st.session_state.user = user

                        

                        st.rerun()

                    else:

                        st.error(
                            "Invalid username/email or password."
                        )


        # =================================================
        # REGISTER
        # =================================================

        with register_tab:

            st.html(
                """
                <div style="
                    margin-top:12px;
                    margin-bottom:18px;
                ">

                    <div style="
                        color:#101828;
                        font-size:21px;
                        font-weight:750;
                    ">
                        Create your account
                    </div>

                    <div style="
                        color:#667085;
                        font-size:12px;
                        margin-top:5px;
                    ">
                        Create a secure account for your workspace.
                    </div>

                </div>
                """
            )


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

                    st.success("Strong password")

                else:

                    st.info(
                        "Use uppercase, lowercase and numbers "
                        "for a stronger password."
                    )


            terms = st.checkbox(
                "I agree to the Terms & Conditions",
                key="terms",
            )


            if st.button(
                "Create Account",
                use_container_width=True,
                type="primary",
                key="register_button",
            ):

                if not full_name:

                    st.error(
                        "Please enter your full name."
                    )

                elif not email or "@" not in email:

                    st.error(
                        "Please enter a valid email."
                    )

                elif not username:

                    st.error(
                        "Please choose a username."
                    )

                elif len(password) < 8:

                    st.error(
                        "Password must contain at least 8 characters."
                    )

                elif password != confirm_password:

                    st.error(
                        "Passwords do not match."
                    )

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
                            "Account created successfully. "
                            "Open the Login tab and sign in."
                        )

                    else:

                        st.error(message)


        st.html(
            """
            <div class="auth-footer-text">
                CodeInsight AI • Secure developer workspace
            </div>
            """
        )



