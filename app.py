import streamlit as st
from PIL import Image
from utils.helpers import get_base64_image
# Correct import statements
from src.pages.chat import chat_main
from src.pages.evolution_days import evolution_days_main
from src.pages.evolution_months import evolution_months_main
from src.pages.holidays import holidays_main
from pages.maps import maps_main
from pages.trips import trips_main
from pages.specific_trips import specific_trips_main
from pages.weather import weather_main

 # OS function to get current relative path
import os
PATH = os.getcwd()  # Get current working directory


@st.cache_data
def apply_background(image_path: str = "files/wallpaper.jpg"):
    # Convert background image to base64
    background_image = get_base64_image(image_path)

    # CSS Styling
    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background: url("data:image/jpg;base64,{background_image}") no-repeat center center fixed;
            background-size: cover;
            color: #ffffff; 
            font-family: 'Poppins', sans-serif;
        }}
        """,
        unsafe_allow_html=True
    )


# Configuración inicial
def setup():

    # CSS Styling
    st.markdown(
        f"""
        <style>
        .header-container {{
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 50vh; /* Ajustar para centrar verticalmente */
            text-align: center;
            background: rgba(0, 0, 0, 0.7);
            color: #ffffff;
        }}
        .header-title {{
            font-size: 3rem;
            font-weight: bold;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
        }}
        .header-subtitle {{
            font-size: 1.5rem;
            margin: 0;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
        }}
        .logo-container {{
            margin-top: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .logo {{
            width: 150px; /* Tamaño reducido para el logo */
        }}
        .cta-buttons {{
            display: flex;
            justify-content: center;
            gap: 25px;
            margin-top: 30px;
        }}
        .cta-button {{
            background-color: #00d2ff;
            color: #ffffff;
            padding: 15px 30px;
            border: none;
            border-radius: 50px;
            font-size: 1.2rem;
            cursor: pointer;
            text-decoration: none;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
            transition: background-color 0.3s ease, transform 0.2s;
        }}
        .cta-button:hover {{
            background-color: #008fb3;
            transform: scale(1.05);
        }}
        .footer {{
            font-family: 'Arial', sans-serif;
            font-size: 0.9rem;
            text-align: center;
            color: #ffffff;
            margin-top: 40px;
            padding: 15px;
            border-top: 2px solid #00d2ff;
            background: #1b263b;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# Función principal
def main():
    setup()  # Configuración inicial

    # Encabezado destacado
    st.markdown(
        f"""
        <div class='header-container'>
            <div class='header-title'>NexMove</div>
            <div class='header-subtitle'>Mobility data at your fingertips</div>
            <div class='logo-container'>
                <img src="data:image/png;base64,{get_base64_image('files/logo.png')}" class='logo' alt='NexMove Logo'>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Espaciador para que el contenido no quede debajo del encabezado fijo
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)

    # Espaciador para que el contenido no quede debajo del encabezado fijo
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)

    # Sección de descripción con desplegables personalizados
    with st.expander("Who are we?", expanded=False):
        st.markdown("We are five students from the UPF Project Management course who have come together, forming a diverse team that combines expertise in Data Science, Audiovisual Engineering, and Telecommunications. Each of us brings a unique technical background, creating a well-rounded group driven by a shared passion for innovation.")

    with st.expander("Web app", expanded=False):
        st.markdown("In our web application all the data is centralized allowing users to interact dynamically via a Chatbot and an interactive interface that enables data extraction and visualization through graphs, charts, and lists.")

    with st.expander("Our mission", expanded=False):
        st.markdown("Our mission is to collaborate with Telefónica on a project that aligns with our studies while exploring our interests in Natural Language Generation and Data Analysis/Visualization. By combining our skills, we want to build a tool that helps Telefónica better organize and understand its data.")

    # Reproducir automaticamente video de youtube
    st.video("https://www.youtube.com/watch?v=SBpZzWt_Wc4", autoplay=True)

    # Pie de página
    st.markdown(
        "<div class='footer'>© 2024 NexMove. All rights reserved.</div>",
        unsafe_allow_html=True
    )


def setup_pages():

    # -- Pages Setup --
    main_page = st.Page(
        main,
        title="Home",
        icon=":material/home:",
        default=True,
    )

    chat_page = st.Page(
        chat_main,
        title="Chat",
        icon=":material/smart_toy:",
    )

    evolution_days_page = st.Page(
        evolution_days_main,
        title="Evolution Days",
        icon=":material/insert_chart_outlined:",
    )

    evolution_months_page = st.Page(
        evolution_months_main,
        title="Evolution Months",
        icon=":material/insert_chart_outlined:",
    )

    holidays_page = st.Page(
        holidays_main,
        title="Holidays",
        icon=":material/calendar_today:",
    )

    maps_page = st.Page(
        maps_main,
        title="Maps",
        icon=":material/map:",
    )

    specific_trips_page = st.Page(
        specific_trips_main,
        title="Specific Trips",
        icon=":material/luggage:",
    )

    trips_page = st.Page(
        trips_main,
        title="Trips",
        icon=":material/directions_bus:",
    )

    weather_page = st.Page(
        weather_main,
        title="Weather",
        icon=":material/wb_sunny:",
    )

    # -- Navigation Setup --
    pages = st.navigation(
        {
            "": [main_page],
            "Interact with the data!": [evolution_days_page,
                                        evolution_months_page,
                                        holidays_page, maps_page,
                                        specific_trips_page,
                                        trips_page, weather_page],
            "Chat with the data!": [chat_page],
        }
    )

    st.set_page_config(
        page_title="NexMove",
        page_icon=":rocket:",
        layout="wide",
        initial_sidebar_state="auto",
    )

    # -- Shared on all pages --
    st.logo("files/logo.png", size='large', link="https://nexmove.streamlit.app")
    apply_background()

    pages.run()

if __name__ == '__main__':
    setup_pages()
