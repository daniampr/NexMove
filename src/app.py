import matplotlib
import streamlit as st
#from chatbot.chatbot import chat_completion
from utils.helpers import DATA
#from src.Pages import evolution


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
    st.write("Description of the app:")
    st.write("Description of the group:")

if __name__ == '__main__':
    matplotlib.use("Agg", force=True)
    main()