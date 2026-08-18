import streamlit as st

from core.analysis.project_chat import ProjectChat


chat = ProjectChat()


def show_repository_chat(project_folder):

    st.subheader("🤖 Repository AI Assistant")

    if "repository_messages" not in st.session_state:
        st.session_state.repository_messages = []

    for message in st.session_state.repository_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask anything about this repository...")

    if prompt:

        st.session_state.repository_messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):

            with st.spinner("Analyzing repository..."):

                try:

                    answer = chat.ask(
                        project_folder,
                        prompt,
                    )

                except Exception as e:

                    answer = f"❌ {e}"

            st.markdown(answer)

        st.session_state.repository_messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

    if st.session_state.repository_messages:

        if st.button(
            "🗑 Clear Chat",
            use_container_width=True,
        ):

            st.session_state.repository_messages = []
            st.rerun()