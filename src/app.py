import streamlit as st
from PIL import Image

# Configuración inicial
def setup():
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(to right, #ffffff, #b3d8ff); /* Degradado blanco a azul claro */
            background-size: cover; /* Asegura que el fondo cubra toda la pantalla */
        }
        .slogan {
            font-family: 'Playfair Display', serif;
            font-size: 1.7rem; /* Tamaño del eslogan */
            font-weight: bold; /* Negrita */
            font-style: italic; /* Cursiva */
            color: #007bff; /* Azul */
            text-align: center;
            margin-top: -20px; /* Ajuste hacia arriba */
            margin-bottom: 30px;
        }
        .expander-header {
            font-family: 'Roboto', sans-serif;
            font-size: 1.3rem;
            color: #007bff;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Función para la página "Home"
def home():
    # Mostrar logo
    try:
        img = Image.open("logo_v2-removebg-preview.png")
        st.image(img, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading image: {e}")
    
    # Mostrar eslogan
    st.markdown(
        "<div class='slogan'>Mobility data at your fingertips</div>",
        unsafe_allow_html=True
    )

    # Desplegables
    with st.expander("¿Quiénes Somos?", expanded=False):
        st.write("Somos un equipo dedicado a proporcionar soluciones innovadoras para la movilidad urbana.")
    
    with st.expander("¿Cómo Funciona Nuestra Web?", expanded=False):
        st.write("Nuestra plataforma permite visualizar datos de movilidad en tiempo real, facilitando la toma de decisiones informadas.")
    
    with st.expander("Nuestra Misión", expanded=False):
        st.write("Nuestra misión es transformar los datos de movilidad en herramientas útiles para mejorar la calidad de vida en las ciudades.")

# Función para la página "Chat"
def chat():
    st.header("Chat")
    st.write("Aquí se implementará el chat.")

# Función para la página "Insights"
def insights():
    st.header("Insights")
    # Crear un selectbox dinámico con los nombres de los archivos de Pages
    subpage = st.selectbox(
        "Selecciona un módulo:",
        ["Evolution", "Evolution1", "Holidays", "Map Pro", "Specific Trips", "Trips", "Weather"]
    )
    
    # Conectar los archivos en Pages
    if subpage == "Evolution":
        from Pages.evolution import app as evolution_app
        evolution_app()
    elif subpage == "Evolution1":
        from Pages.evolution1 import app as evolution1_app
        evolution1_app()
    elif subpage == "Holidays":
        from Pages.holidays import app as holidays_app
        holidays_app()
    elif subpage == "Map Pro":
        from Pages.map_pro import app as map_pro_app
        map_pro_app()
    elif subpage == "Specific Trips":
        from Pages.specific_trips import app as specific_trips_app
        specific_trips_app()
    elif subpage == "Trips":
        from Pages.trips import app as trips_app
        trips_app()
    elif subpage == "Weather":
        from Pages.weather import app as weather_app
        weather_app()

# Función principal
def main():
    setup()  # Configuración inicial

    # Crear sidebar con pestañas
    menu = st.sidebar.radio(
        "Navegación",
        ["Home 🏠", "Chat", "Insights"]
    )

    # Navegación entre las pestañas
    if menu == "Home 🏠":
        home()
    elif menu == "Chat":
        chat()
    elif menu == "Insights":
        insights()

if __name__ == '__main__':
    main()
