import streamlit as st
from utils.helpers import get_base64_image, setup_headers
# Correct import statements
from pages.chat import chat_main
from pages.evolution_days import evolution_days_main
from pages.evolution_months import evolution_months_main
from pages.holidays import holidays_main
from pages.maps import maps_main
from pages.trips import trips_main
from pages.specific_trips import specific_trips_main
from pages.weather import weather_main


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


# Función principal
def main():
    setup_headers()  # Configuración inicial

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
