import streamlit as st

from core.analysis.project_chat import ProjectChat


chat = ProjectChat()


def show_project_chat(project_folder):

    st.subheader("💬 Chat With Project")

    question = st.text_input(

        "Ask anything about this project"

    )

    if st.button("Ask AI"):

        if not question:

            st.warning("Enter a question.")

            return

        with st.spinner("Analyzing Project..."):

            try:

                answer = chat.ask(

                    project_folder,

                    question,

                )

                st.markdown(answer)

            except Exception as e:

                st.error(e)