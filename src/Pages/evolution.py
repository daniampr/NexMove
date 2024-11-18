import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import base64
from utils.helpers import DATA

# Function to encode image to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Configuración inicial
def setup():
    st.set_page_config(
        page_title="Evolution",
        page_icon="🔄",  # Icono de evolución
        layout="wide",
    )

    # Convert background image to base64
    background_image = get_base64_image("starrynight_5.jpg")

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
            height: 30vh; /* Ajustar para centrar verticalmente */
            text-align: center;
            background: rgba(0, 0, 0, 0.7);
            color: #ffffff;
            margin-bottom: 30px;
        }}
        .header-title {{
            font-size: 2.5rem;
            font-weight: bold;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
        }}
        .header-subtitle {{
            font-size: 1.5rem;
            margin: 0;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
        }}
        .divider {{
            border-top: 3px solid #00d2ff; /* Divider estilo NexMove */
            margin: 20px 0;
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
     /* Streamlit Selectbox Styling */
        div[data-baseweb="select"] > div {{
            background-color: #ffffff !important; /* White background */
            color: #000000 !important; /* Black text */
            border: 1px solid #00d2ff !important; /* NexMove blue border */
            border-radius: 5px !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Función principal
def main():
    setup()  # Configuración inicial

    # Títulos principales
    st.markdown(
        """
        <div class='header-container'>
            <div class='header-title'>NexMove: Data Evolution</div>
            <div class='header-subtitle'>Interactive Insights Over the Years</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Asegurarse de que 'day' esté en formato datetime
    DATA['day'] = pd.to_datetime(DATA['day'], errors='coerce')

    # Agrupar por año y mes, luego sumar la columna 'viajeros'
    monthly_travelers = DATA.groupby(['year', 'month'])['viajeros'].sum().reset_index()

    # Crear una tabla pivote con 'month' como índice y columnas como años
    pivoted_data = monthly_travelers.pivot(index='month', columns='year', values='viajeros')

    # 1. Mostrar gráfico combinado de todos los años
    st.write("## Total Number of Travelers per Month (Comparison by Year)")
    st.line_chart(pivoted_data)

    # 2. Mostrar gráficos individuales por año, organizados en columnas
    years = monthly_travelers['year'].unique()
    cols = st.columns(len(years))  # Crear una columna para cada año

    for i, year in enumerate(years):
        with cols[i]:  # Usar cada columna para un año
            st.write(f"### Total Travelers per Month in {year}")
            year_data = monthly_travelers[monthly_travelers['year'] == year].set_index('month')
            st.line_chart(year_data[['viajeros']])

# Add the title for province insights
st.write("## Insights for each province (origin & destination)")

    # Obtener provincias únicas para origen y destino
    origin_provinces = DATA['provincia_origen_name'].unique()
    destination_provinces = DATA['provincia_destino_name'].unique()

    col1, col2 = st.columns(2)  # Crear dos columnas para origen y destino

    # Selección y gráfico de provincia de origen
    with col1:
        selected_province = st.selectbox("Select Origin Province", origin_provinces)
        province_data = DATA[DATA['provincia_origen_name'] == selected_province]
        monthly_travelers_origin = province_data.groupby(['year', 'month'])['viajeros'].sum().reset_index()

        st.write(f"### Travelers per Month (Origin: {selected_province})")

        # Mostrar gráfico por año
        for year in years:
            st.write(f"#### {year}")
            year_data = monthly_travelers_origin[monthly_travelers_origin['year'] == year].set_index('month')
            st.line_chart(year_data[['viajeros']])

    # Selección y gráfico de provincia de destino
    with col2:
        selected_province_destino = st.selectbox("Select Destination Province", destination_provinces)
        province_data_destino = DATA[DATA['provincia_destino_name'] == selected_province_destino]
        monthly_travelers_destino = province_data_destino.groupby(['year', 'month'])['viajeros'].sum().reset_index()

        st.write(f"### Travelers per Month (Destination: {selected_province_destino})")

        # Mostrar gráfico por año
        for year in years:
            st.write(f"#### {year}")
            year_data = monthly_travelers_destino[monthly_travelers_destino['year'] == year].set_index('month')
            st.line_chart(year_data[['viajeros']])

# Add the title for community insights
st.write("## Insights for each Autonomous Community (origin & destination)")

    # Obtener comunidades únicas para origen y destino
    origin_communities = DATA['comunidad_origen'].unique()
    destination_communities = DATA['comunidad_destino'].unique()

    col3, col4 = st.columns(2)  # Crear dos columnas para origen y destino comunidad

    # Selección y gráfico de comunidad de origen
    with col3:
        selected_community = st.selectbox("Select Origin Autonomous Community", origin_communities)
        community_data = DATA[DATA['comunidad_origen'] == selected_community]
        monthly_travelers_origin_community = community_data.groupby(['year', 'month'])['viajeros'].sum().reset_index()

        st.write(f"### Travelers per Month (Origin Community: {selected_community})")
        # Mostrar gráfico por año
        for year in years:
            st.write(f"#### {year}")
            year_data = monthly_travelers_origin_community[monthly_travelers_origin_community['year'] == year].set_index('month')
            st.line_chart(year_data[['viajeros']])

    # Selección y gráfico de comunidad de destino
    with col4:
        selected_community_destino = st.selectbox("Select Destination Autonomous Community", destination_communities)
        community_data_destino = DATA[DATA['comunidad_destino'] == selected_community_destino]
        monthly_travelers_destino_community = community_data_destino.groupby(['year', 'month'])['viajeros'].sum().reset_index()

        st.write(f"### Travelers per Month (Destination Community: {selected_community_destino})")
        # Mostrar gráfico por año
        for year in years:
            st.write(f"#### {year}")
            year_data = monthly_travelers_destino_community[monthly_travelers_destino_community['year'] == year].set_index('month')
            st.line_chart(year_data[['viajeros']])
