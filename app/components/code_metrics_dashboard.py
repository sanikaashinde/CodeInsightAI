import streamlit as st
import pandas as pd


def show_code_metrics_dashboard(

    quality,

    security,

    complexity,

    repository,

    duplicates,

    dead_code,

    todos,

):

    st.subheader("📈 Enterprise Code Metrics Dashboard")

    # ============================================
    # KPIs
    # ============================================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(

        "Quality",

        f"{quality['overall']}/100"

    )

    c2.metric(

        "Security",

        f"{security:.1f}/100"

    )

    c3.metric(

        "Avg Complexity",

        complexity

    )

    duplicate_pairs = duplicates["summary"]["duplicate_pairs"]

    c4.metric(

        "Duplicate Files",

        duplicate_pairs

    )

    st.divider()

    # ============================================
    # Progress Bars
    # ============================================

    st.markdown("### Overall Scores")

    st.metric(

        "Documentation",

        f"{quality['documentation']}%"

    )

    st.progress(

        quality["documentation"] / 100

    )

    st.metric(

        "Maintainability",

        f"{quality['maintainability']}%"

    )

    st.progress(

        quality["maintainability"] / 100

    )

    st.metric(

        "Readability",

        f"{quality['readability']}%"

    )

    st.progress(

        quality["readability"] / 100

    )

    st.metric(

        "Architecture",

        f"{quality['architecture']}%"

    )

    st.progress(

        quality["architecture"] / 100

    )

    st.divider()

    # ============================================
    # Project Statistics
    # ============================================

    stats = repository["statistics"]

    st.markdown("### Repository Statistics")

    r1, r2, r3 = st.columns(3)

    r1.metric(

        "Files",

        stats["files"]

    )

    r2.metric(

        "Lines",

        stats["lines"]

    )

    r3.metric(

        "Code Lines",

        stats["code_lines"]

    )

    r4, r5, r6 = st.columns(3)

    r4.metric(

        "Blank Lines",

        stats["blank_lines"]

    )

    r5.metric(

        "Comments",

        stats["comment_lines"]

    )

    r6.metric(

        "Avg File Size",

        stats["average_file_size"]

    )

    st.divider()

    # ============================================
    # Languages
    # ============================================

    st.markdown("### Language Distribution")

    lang_df = pd.DataFrame(

        {

            "Language": repository["languages"].keys(),

            "Files": repository["languages"].values(),

        }

    )

    if not lang_df.empty:

        st.bar_chart(

            lang_df.set_index("Language")

        )

    st.divider()

    # ============================================
    # Dead Code
    # ============================================

    st.markdown("### Dead Code")

    d1, d2, d3, d4 = st.columns(4)

    d1.metric(

        "Functions",

        dead_code["summary"]["functions"]

    )

    d2.metric(

        "Classes",

        dead_code["summary"]["classes"]

    )

    d3.metric(

        "Imports",

        dead_code["summary"]["imports"]

    )

    d4.metric(

        "Variables",

        dead_code["summary"]["variables"]

    )

    st.divider()

    # ============================================
    # TODO
    # ============================================

    st.markdown("### TODO / FIXME")

    t1, t2 = st.columns(2)

    t1.metric(

        "Pending Items",

        todos["summary"]["total"]

    )

    t2.metric(

        "Files",

        todos["summary"]["files"]

    )

    st.divider()

    # ============================================
    # Largest Files
    # ============================================

    st.markdown("### Largest Files")

    st.dataframe(

        repository["largest_files"],

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    # ============================================
    # Final Grade
    # ============================================

    grade = "A+"

    if quality["overall"] < 90:

        grade = "A"

    if quality["overall"] < 80:

        grade = "B"

    if quality["overall"] < 70:

        grade = "C"

    if quality["overall"] < 60:

        grade = "D"

    st.success(

        f"🏆 Overall Repository Grade : {grade}"

    )