import matplotlib
import streamlit as st
#from chatbot.chatbot import chat_completion
from utils.helpers import DATA
#from src.Pages import evolution
from PIL import Image 


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


    try:
        # Open the image file
        img = Image.open("logo_v2-removebg-preview.png")
        # Display the image
        st.image(img, use_container_width=True)  # use_column_width will make the image span the width of the app
    except Exception as e:
        st.error(f"Error loading image: {e}")

    st.write("Description of the app:")
    st.write("Description of the group:")


if __name__ == '__main__':
    matplotlib.use("Agg", force=True)
    main()