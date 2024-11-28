import streamlit as st
from PIL import Image
import base64


# Function to encode image to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


# Configuración inicial
def setup():
    st.set_page_config(
        page_title="NexMove",
        page_icon="🚀",  # Icono de cohete
        layout="wide",
    )

    # Convert background image to base64
    background_image = get_base64_image("wallpaper.jpg")

    # CSS Styling
    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background: url("data:image/jpg;base64,{background_image}") no-repeat center center fixed;
            background-size: cover;
            color: #ffffff; /* Texto blanco */
            font-family: 'Poppins', sans-serif;
        }}
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
                <img src="data:image/png;base64,{get_base64_image('logo_v2-removebg-preview.png')}" class='logo' alt='NexMove Logo'>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

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


if __name__ == '__main__':
    main()
