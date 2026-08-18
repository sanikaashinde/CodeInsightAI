import streamlit as st


def show_documentation_dashboard(result):

    st.subheader("📚 Documentation Analysis")

    # =====================================================
    # Summary
    # =====================================================

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Documentation Grade",
        result["grade"],
    )

    c2.metric(
        "Overall Coverage",
        f"{result['overall']}%",
    )

    c3.metric(
        "README",
        "✅ Present" if result["readme"] else "❌ Missing",
    )

    st.progress(result["overall"] / 100)

    # =====================================================
    # Coverage Breakdown
    # =====================================================

    st.divider()

    st.markdown("### 📈 Coverage Breakdown")

    b1, b2, b3 = st.columns(3)

    with b1:

        st.metric(
            "Functions",
            f"{result['function_coverage']}%",
        )

        st.progress(
            result["function_coverage"] / 100
        )

    with b2:

        st.metric(
            "Classes",
            f"{result['class_coverage']}%",
        )

        st.progress(
            result["class_coverage"] / 100
        )

    with b3:

        st.metric(
            "Modules",
            f"{result['module_coverage']}%",
        )

        st.progress(
            result["module_coverage"] / 100
        )

    # =====================================================
    # Statistics
    # =====================================================

    st.divider()

    st.markdown("### 📊 Documentation Statistics")

    s1, s2 = st.columns(2)

    with s1:

        st.metric(
            "Functions",
            result["total_functions"],
        )

        st.metric(
            "Documented Functions",
            result["documented_functions"],
        )

    with s2:

        st.metric(
            "Classes",
            result["total_classes"],
        )

        st.metric(
            "Documented Classes",
            result["documented_classes"],
        )

    # =====================================================
    # Missing Function Docs
    # =====================================================

    if result["missing_functions"]:

        st.divider()

        st.markdown(
            "### ❌ Functions Missing Docstrings"
        )

        st.dataframe(
            result["missing_functions"],
            use_container_width=True,
            hide_index=True,
        )

    # =====================================================
    # Missing Class Docs
    # =====================================================

    if result["missing_classes"]:

        st.divider()

        st.markdown(
            "### ❌ Classes Missing Docstrings"
        )

        st.dataframe(
            result["missing_classes"],
            use_container_width=True,
            hide_index=True,
        )

    # =====================================================
    # Suggestions
    # =====================================================

    st.divider()

    st.markdown("### 💡 Improvement Suggestions")

    if result["suggestions"]:

        for suggestion in result["suggestions"]:

            st.write(f"• {suggestion}")

    else:

        st.success(
            "Excellent documentation quality."
        )

    # =====================================================
    # Final Status
    # =====================================================

    st.divider()

    if result["grade"] == "A":

        st.success(
            "🏆 Enterprise-grade documentation."
        )

    elif result["grade"] == "B":

        st.info(
            "✅ Good documentation."
        )

    elif result["grade"] == "C":

        st.warning(
            "⚠ Documentation should be improved."
        )

    else:

        st.error(
            "❌ Poor documentation coverage."
        )