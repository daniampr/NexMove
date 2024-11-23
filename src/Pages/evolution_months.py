import streamlit as st
import numpy as np
import pandas as pd
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
        page_icon="🔄",
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
            color: #ffffff;
            font-family: 'Poppins', sans-serif;
        }}
        .header-container {{
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 30vh;
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
            border-top: 3px solid #00d2ff;
            margin: 20px 0;
        }}
        div[data-testid="stHorizontalBlock"] {{
            display: flex;
            justify-content: center;
            align-items: flex-start;
            gap: 20px;
        }}
        div[data-testid="stBlock"] {{
            margin-bottom: 30px;
        }}
        div[data-testid="stSelectbox"] > label {{
            color: #ffffff !important;
            font-size: 16px;
            font-weight: bold;
        }}
        div[data-baseweb="select"] > div {{
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 1px solid #00d2ff !important;
            border-radius: 5px !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Main function
def main():
    setup()

    # Main Title
    st.markdown("<h2 class='header-title'>INTERACTIVE DATA: EVOLUTION OVER THE YEARS</h2>", unsafe_allow_html=True)

    # Divider
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Ensure 'day' is in datetime format
    DATA['day'] = pd.to_datetime(DATA['day'], errors='coerce')

    # Aggregate by year and month, then sum the 'viajeros' column
    monthly_travelers = DATA.groupby(['year', 'month'])['viajeros'].sum().reset_index()

    # Create a pivot table with 'month' as rows and 'year' as columns
    pivoted_data = monthly_travelers.pivot(index='month', columns='year', values='viajeros')

    # Combined chart for all years
    st.write("<h3 style='text-align: center;'>Total Number of Travelers per Month (Comparison by Year)</h3>", unsafe_allow_html=True)
    st.line_chart(pivoted_data)

    # Individual charts for each year
    years = monthly_travelers['year'].unique()
    cols = st.columns(len(years))  # Create one column per year

    for i, year in enumerate(years):
        with cols[i]:
            st.markdown(f"<h4 style='text-align: center;'>Travelers in {year}</h4>", unsafe_allow_html=True)
            year_data = monthly_travelers[monthly_travelers['year'] == year].set_index('month')
            st.line_chart(year_data[['viajeros']])

    st.divider()

    # Province-level insights
    st.write("<h3 style='text-align: center;'>Insights for Each Province (Origin & Destination)</h3>", unsafe_allow_html=True)

    # Unique provinces for origin and destination
    origin_provinces = DATA['provincia_origen_name'].unique()
    destination_provinces = DATA['provincia_destino_name'].unique()

    col1, col2 = st.columns(2)

    with col1:
        selected_province = st.selectbox("Select Origin Province", origin_provinces)
        province_data = DATA[DATA['provincia_origen_name'] == selected_province]
        monthly_travelers_origin = province_data.groupby(['year', 'month'])['viajeros'].sum().reset_index()
        st.write(f"<h4 style='text-align: center;'>Travelers per Month (Origin: {selected_province})</h4>", unsafe_allow_html=True)
        for year in years:
            year_data = monthly_travelers_origin[monthly_travelers_origin['year'] == year].set_index('month')
            st.line_chart(year_data[['viajeros']])

    with col2:
        selected_province_destino = st.selectbox("Select Destination Province", destination_provinces)
        province_data_destino = DATA[DATA['provincia_destino_name'] == selected_province_destino]
        monthly_travelers_destino = province_data_destino.groupby(['year', 'month'])['viajeros'].sum().reset_index()
        st.write(f"<h4 style='text-align: center;'>Travelers per Month (Destination: {selected_province_destino})</h4>", unsafe_allow_html=True)
        for year in years:
            year_data = monthly_travelers_destino[monthly_travelers_destino['year'] == year].set_index('month')
            st.line_chart(year_data[['viajeros']])

    st.divider()

    # Autonomous community insights
    st.write("<h3 style='text-align: center;'>Insights for Each Autonomous Community (Origin & Destination)</h3>", unsafe_allow_html=True)

    # Unique communities for origin and destination
    origin_communities = DATA['comunidad_origen'].unique()
    destination_communities = DATA['comunidad_destino'].unique()

    col3, col4 = st.columns(2)

    with col3:
        selected_community = st.selectbox("Select Origin Autonomous Community", origin_communities)
        community_data = DATA[DATA['comunidad_origen'] == selected_community]
        monthly_travelers_origin_community = community_data.groupby(['year', 'month'])['viajeros'].sum().reset_index()
        st.write(f"<h4 style='text-align: center;'>Travelers per Month (Origin Community: {selected_community})</h4>", unsafe_allow_html=True)
        for year in years:
            year_data = monthly_travelers_origin_community[monthly_travelers_origin_community['year'] == year].set_index('month')
            st.line_chart(year_data[['viajeros']])

    with col4:
        selected_community_destino = st.selectbox("Select Destination Autonomous Community", destination_communities)
        community_data_destino = DATA[DATA['comunidad_destino'] == selected_community_destino]
        monthly_travelers_destino_community = community_data_destino.groupby(['year', 'month'])['viajeros'].sum().reset_index()
        st.write(f"<h4 style='text-align: center;'>Travelers per Month (Destination Community: {selected_community_destino})</h4>", unsafe_allow_html=True)
        for year in years:
            year_data = monthly_travelers_destino_community[monthly_travelers_destino_community['year'] == year].set_index('month')
            st.line_chart(year_data[['viajeros']])

if __name__ == '__main__':
    main()
