import streamlit as st
from chatbot.chat_helpers import chat_completion
from utils.helpers import DATA_simple_chat

# Constants
MODELS = ["gpt-4o-mini", "mixtral-8x7b-32768", "llama-3.2-3b-preview"]


def chat_main():
    # Set the title and description
    st.title("NexMove: Mobility Data at Your Fingertips")

    # with st.expander("ℹ️ Disclaimer"):
    #    st.caption(
    #        """
    #        We appreciate your engagement! This chatbot provides insights into mobility data.
    #        Please note, the demo version may have limitations based on usage. Thank you for understanding.
    #        """
    #    )

    # Initialize session state for messages and selected model
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Data preview section
    st.subheader("Data Preview")
    st.write(DATA_simple_chat)

    # Model selection dropdown
    model = st.selectbox(
        "Select model ",
        MODELS,
        key="selected_model",
        label_visibility="collapsed"
    )

    # Display existing chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Limit the number of messages to prevent excessive usage
    max_messages = 20  # 10 user-assistant exchanges

    if len(st.session_state.messages) >= max_messages:
        st.info(
            """
            Notice: The maximum message limit for this version has been reached. We value your interest!
            Refresh the page to start a new chat session.
            """
        )
    else:
        # Chat input box
        if prompt := st.chat_input("Ask me anything about the data!"):
            # Add user message to session state
            st.session_state.messages.append({
                "role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        
                        response, code_executed = chat_completion(prompt, model)
                        st.markdown(response)  # Display the assistant's response
                        st.session_state.messages.append(
                            {"role": "assistant", "content": response}
                        )

                        # Optionally display the executed code
                        with st.expander("🔍 View code executed"):
                            st.code(code_executed)

                    except Exception as e:
                        error_message = "Oops! An error occurred while processing your request."
                        st.error(f"{error_message}: {str(e)}")
                        st.session_state.messages.append(
                            {"role": "assistant", "content": error_message}
                        )
