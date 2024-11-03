import matplotlib
import streamlit as st
from chatbot.chatbot import chat_completion
from utils.helpers import DATA


def setup():
    st.header(
        "NexMove: Mobility data at your fingertips",
        anchor=False, divider="red"
    )
    
    hide_menu_style = """
            <style>
            #MainMenu {visibility: hidden;}
            </style>
            """
    st.markdown(hide_menu_style, unsafe_allow_html=True)


def main():
    setup()

    st.write("Data Preview:")
    st.write(DATA)
    prompt = st.text_input(
        "Ask me anything about the data!",  # Input label
        placeholder="Tell me the average number of displacements in 2023."
    )
    if not prompt:
        st.stop()
    st.write("🧞‍♂️ Here's what I found:")
    response, code_executed = chat_completion(prompt)
    st.divider()
    st.write("🧞‍♂️ Under the hood, the code that was executed:")
    st.code(code_executed)


if __name__ == '__main__':
    matplotlib.use("Agg", force=True)
    main()
