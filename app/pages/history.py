import streamlit as st

from core.auth import (
    get_analysis_history,
    save_analysis_history,
    clear_analysis_history,
)


def add_analysis_history(
    analysis_type,
    name,
    quality_score=None,
    security_score=None,
    complexity=None,
    functions=None,
    classes=None,
    code_smells=None,
):
    user = st.session_state.get("user")

    if not user:
        return

    from datetime import datetime

    time = datetime.now().strftime(
        "%d %b %Y, %I:%M %p"
    )

    save_analysis_history(
        user_id=user["id"],
        analysis_type=analysis_type,
        name=name,
        quality_score=quality_score,
        security_score=security_score,
        complexity=complexity,
        functions=functions,
        classes=classes,
        code_smells=code_smells,
        time=time,
    )


def show_history():

    user = st.session_state.get("user")

    if not user:
        st.error("Please login to view analysis history.")
        return

    history = get_analysis_history(user["id"])

    st.title("🕘 Analysis History")

    st.caption(
        f"Previous analyses for {user['full_name']}"
    )

    # =====================================================
    # EMPTY STATE
    # =====================================================

    if not history:

        st.divider()

        st.markdown(
            """
            <div style="
                text-align:center;
                padding:55px 20px;
                border:1px solid rgba(128,128,128,0.20);
                border-radius:16px;
                margin-top:20px;
            ">
                <div style="font-size:48px;">🕘</div>
                <h3>No Analysis History Yet</h3>
                <p style="color:#888;">
                    Analyze a project or paste code to start
                    building your analysis history.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        return

    # =====================================================
    # SUMMARY
    # =====================================================

    total = len(history)

    quality_values = [
        x["quality_score"]
        for x in history
        if x["quality_score"] is not None
    ]

    security_values = [
        x["security_score"]
        for x in history
        if x["security_score"] is not None
    ]

    avg_quality = (
        round(
            sum(quality_values) / len(quality_values),
            1,
        )
        if quality_values
        else "N/A"
    )

    avg_security = (
        round(
            sum(security_values) / len(security_values),
            1,
        )
        if security_values
        else "N/A"
    )

    st.subheader("📊 Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Total Analyses", total)

    with c2:
        st.metric(
            "Avg Quality",
            f"{avg_quality}/100"
            if avg_quality != "N/A"
            else "N/A",
        )

    with c3:
        st.metric(
            "Avg Security",
            f"{avg_security}/100"
            if avg_security != "N/A"
            else "N/A",
        )

    with c4:
        st.metric(
            "Latest",
            history[0].get("time", "N/A"),
        )

    st.divider()

    # =====================================================
    # FILTER + CLEAR
    # =====================================================

    st.subheader("🔎 Browse Analyses")

    col1, col2 = st.columns([3, 1])

    analysis_types = sorted(
        set(
            item.get("type", "Analysis")
            for item in history
        )
    )

    with col1:

        selected_type = st.selectbox(
            "Filter by analysis type",
            ["All"] + analysis_types,
            label_visibility="collapsed",
        )

    with col2:

        if st.button(
            "🗑️ Clear History",
            use_container_width=True,
        ):

            clear_analysis_history(user["id"])

            st.success(
                "Analysis history cleared."
            )

            st.rerun()

    if selected_type == "All":

        filtered_history = history

    else:

        filtered_history = [
            item
            for item in history
            if item.get("type") == selected_type
        ]

    st.caption(
        f"Showing {len(filtered_history)} of {total} analyses"
    )

    # =====================================================
    # HISTORY CARDS
    # =====================================================

    for index, item in enumerate(filtered_history):

        analysis_type = item.get(
            "type",
            "Analysis",
        )

        name = item.get(
            "name",
            "Unnamed Analysis",
        )

        time = item.get(
            "time",
            "",
        )

        quality = item.get("quality_score")
        security = item.get("security_score")
        complexity = item.get("complexity")
        functions = item.get("functions")
        classes = item.get("classes")
        smells = item.get("code_smells")

        with st.expander(
            f"{analysis_type} • {name} • {time}",
            expanded=False,
        ):

            m1, m2, m3, m4 = st.columns(4)

            with m1:
                st.metric(
                    "Quality",
                    f"{quality}/100"
                    if quality is not None
                    else "N/A",
                )

            with m2:
                st.metric(
                    "Security",
                    f"{security}/100"
                    if security is not None
                    else "N/A",
                )

            with m3:
                st.metric(
                    "Avg Complexity",
                    complexity
                    if complexity is not None
                    else "N/A",
                )

            with m4:
                st.metric(
                    "Functions",
                    functions
                    if functions is not None
                    else "N/A",
                )

            st.divider()

            d1, d2, d3 = st.columns(3)

            with d1:
                st.markdown("**🏛️ Classes**")
                st.write(
                    classes
                    if classes is not None
                    else "N/A"
                )

            with d2:
                st.markdown("**🧹 Code Smells**")
                st.write(
                    smells
                    if smells is not None
                    else "N/A"
                )

            with d3:
                st.markdown("**📅 Analyzed On**")
                st.write(time or "N/A")

            if quality is not None:

                if quality >= 80:
                    st.success(
                        "Quality assessment: Excellent"
                    )

                elif quality >= 60:
                    st.warning(
                        "Quality assessment: Good, with room for improvement"
                    )

                else:
                    st.error(
                        "Quality assessment: Needs improvement"
                    )

            st.caption(
                "CodeInsight AI • Analysis Record"
            )

    st.divider()

    st.caption(
        "Only the latest 20 analysis records are retained per user."
    )

