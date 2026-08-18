import streamlit as st


def show_technical_debt(result):

    st.subheader("💳 Technical Debt Analysis")

    score = result["score"]
    cleanup = result["cleanup_hours"]
    risk = result["risk"]

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Technical Debt",
        f"{score}/100",
    )

    c2.metric(
        "Cleanup Time",
        f"{cleanup} hrs",
    )

    c3.metric(
        "Risk",
        risk,
    )

    st.progress(min(score, 100) / 100)

    # ===========================================
    # Risk Indicator
    # ===========================================

    if risk == "LOW":

        st.success("🟢 Low Technical Debt")

    elif risk == "MEDIUM":

        st.warning("🟡 Medium Technical Debt")

    elif risk == "HIGH":

        st.error("🟠 High Technical Debt")

    else:

        st.error("🔴 Critical Technical Debt")

    st.divider()

    # ===========================================
    # Breakdown
    # ===========================================

    st.markdown("### 📊 Debt Breakdown")

    b1, b2 = st.columns(2)

    with b1:

        st.metric(
            "Documentation",
            f"{result['documentation']}%",
        )

        st.metric(
            "Security Issues",
            result["security_issues"],
        )

    with b2:

        st.metric(
            "High Complexity",
            result["high_complexity"],
        )

        st.metric(
            "Code Smells",
            result["code_smells"],
        )

    st.metric(
        "Large Files",
        result["large_files"],
    )

    st.divider()

    # ===========================================
    # Reasons
    # ===========================================

    st.markdown("### 📋 Why this Technical Debt?")

    if result["reasons"]:

        for reason in result["reasons"]:

            st.write(f"• {reason}")

    else:

        st.success("No significant technical debt detected.")