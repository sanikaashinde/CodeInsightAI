import streamlit as st

from core.analysis.repository_search import RepositorySearch


search_engine = RepositorySearch()


# ==========================================================
# REPOSITORY SEARCH UI
# ==========================================================

def show_repository_search(project_folder):

    st.subheader("🔍 Repository Search")

    keyword = st.text_input(
        "Search code, class, function, variable..."
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        case_sensitive = st.checkbox(
            "Case Sensitive"
        )

    with c2:

        whole_word = st.checkbox(
            "Whole Word"
        )

    with c3:

        regex = st.checkbox(
            "Regex"
        )

    if st.button(
        "🔎 Search Repository",
        use_container_width=True
    ):

        if not keyword.strip():

            st.warning(
                "Please enter a keyword."
            )

            return

        with st.spinner(
            "Searching repository..."
        ):

            results = search_engine.search(

                project_folder,

                keyword,

                case_sensitive=case_sensitive,

                regex=regex,

                whole_word=whole_word,

            )

        stats = search_engine.statistics(
            results
        )

        st.success(

            f"Found {stats['matches']} matches "
            f"in {stats['files']} files "
            f"({stats['search_time']} sec)"

        )

        # ==================================================

        # TOP FILES

        # ==================================================

        top = search_engine.top_files(
            results
        )

        if top:

            st.markdown(
                "### 📂 Most Matching Files"
            )

            table = []

            for file, count in top:

                table.append({

                    "File": file,

                    "Matches": count

                })

            st.dataframe(

                table,

                use_container_width=True,

                hide_index=True

            )

        # ==================================================

        # RESULTS

        # ==================================================

        if results:

            st.markdown(
                "### 📄 Search Results"
            )

            for item in results:

                with st.expander(

                    f"{item['file']}  •  Line {item['line']}"

                ):

                    st.code(

                        item["content"],

                        language="python"

                    )

        else:

            st.info(
                "No matching code found."
            )

        # ==================================================

        # EXPORT

        # ==================================================

        md = search_engine.export_markdown(
            results
        )

        st.download_button(

            label="⬇ Download Search Report",

            data=md,

            file_name="repository_search.md",

            mime="text/markdown",

            use_container_width=True

        )