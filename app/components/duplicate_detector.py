import streamlit as st

from core.analysis.duplicate_detector import DuplicateCodeDetector


def show_duplicate_detector(project_folder):

    analyzer = DuplicateCodeDetector()

    duplicates = analyzer.analyze(project_folder)

    summary = analyzer.summary(duplicates)

    st.subheader("👯 Duplicate Code Detector")

    c1, c2 = st.columns(2)

    c1.metric(
        "Duplicate Pairs",
        summary["duplicate_pairs"]
    )

    c2.metric(
        "Highest Similarity",
        f"{summary['highest_similarity']}%"
    )

    st.divider()

    if not duplicates:

        st.success("✅ No duplicate code detected.")

        return

    st.warning(
        f"Found {summary['duplicate_pairs']} duplicate code pairs."
    )

    table = []

    for duplicate in duplicates:

        table.append(

            {

                "File 1": duplicate["file_1"],

                "File 2": duplicate["file_2"],

                "Similarity (%)": duplicate["similarity"],

            }

        )

    st.dataframe(

        table,

        hide_index=True,

        use_container_width=True,

    )

    st.download_button(

        label="⬇ Download Duplicate Report",

        data=_export_markdown(duplicates),

        file_name="duplicate_code_report.md",

        mime="text/markdown",

        use_container_width=True,

    )


def _export_markdown(duplicates):

    md = "# Duplicate Code Report\n\n"

    if not duplicates:

        md += "No duplicate code detected.\n"

        return md

    md += "| File 1 | File 2 | Similarity |\n"

    md += "|--------|--------|------------|\n"

    for duplicate in duplicates:

        md += (

            f"| {duplicate['file_1']} "

            f"| {duplicate['file_2']} "

            f"| {duplicate['similarity']}% |\n"

        )

    return md