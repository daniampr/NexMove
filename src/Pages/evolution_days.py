import streamlit as st
import pandas as pd
from utils.helpers import DATA

# Function to encode image to base64
def get_base64_image(image_path):
    import base64
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Configuración inicial
def setup():
    st.set_page_config(
        page_title="Day of the Week Analysis",
        page_icon="📅",  # Icono de calendario
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
    st.markdown("<h2 class='subtitle'>INTERACTIVE DATA: EVOLUTION BY DAY OF THE WEEK</h2>", unsafe_allow_html=True)

    # Línea divisoria
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Ensure 'day_of_week' is properly categorized
    day_of_week_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    DATA['day_of_week'] = pd.Categorical(DATA['day_of_week'], categories=day_of_week_order, ordered=True)

    # Aggregate travelers by year and day of the week
    weekly_travelers = DATA.groupby(['year', 'day_of_week'])['viajeros'].sum().reset_index()

    # Create a pivot table with 'day_of_week' as rows and years as columns
    pivoted_data = weekly_travelers.pivot(index='day_of_week', columns='year', values='viajeros')

    # 1. Combined chart for all years
    st.write("## Total Number of Travelers per Day of the Week (Comparison by Year)")
    st.line_chart(pivoted_data)

    # 2. Individual charts for each year in separate columns
    years = weekly_travelers['year'].unique()
    cols = st.columns(len(years))

    for i, year in enumerate(years):
        with cols[i]:  # Display each year's data in a separate column
            st.write(f"### Total Travelers by Day of the Week in {year}")
            year_data = weekly_travelers[weekly_travelers['year'] == year].set_index('day_of_week')
            st.line_chart(year_data[['viajeros']])

    st.divider()

    # Province-level insights
    st.write("## Insights for Each Province (Origin & Destination)")

    origin_provinces = DATA['provincia_origen_name'].unique()
    destination_provinces = DATA['provincia_destino_name'].unique()

    col1, col2 = st.columns(2)

    # Origin province analysis
    with col1:
        selected_province = st.selectbox("Select Origin Province", origin_provinces)
        province_data = DATA[DATA['provincia_origen_name'] == selected_province]
        weekly_travelers_origin = province_data.groupby(['year', 'day_of_week'])['viajeros'].sum().reset_index()

        st.write(f"### Travelers by Day of the Week (Origin: {selected_province})")
        for year in years:
            st.write(f"#### {year}")
            year_data = weekly_travelers_origin[weekly_travelers_origin['year'] == year].set_index('day_of_week')
            st.line_chart(year_data[['viajeros']])

    # Destination province analysis
    with col2:
        selected_province_destino = st.selectbox("Select Destination Province", destination_provinces)
        province_data_destino = DATA[DATA['provincia_destino_name'] == selected_province_destino]
        weekly_travelers_destino = province_data_destino.groupby(['year', 'day_of_week'])['viajeros'].sum().reset_index()

        st.write(f"### Travelers by Day of the Week (Destination: {selected_province_destino})")
        for year in years:
            st.write(f"#### {year}")
            year_data = weekly_travelers_destino[weekly_travelers_destino['year'] == year].set_index('day_of_week')
            st.line_chart(year_data[['viajeros']])

    st.divider()

    # Autonomous community insights
    st.write("## Insights for Each Autonomous Community (Origin & Destination)")

    origin_communities = DATA['comunidad_origen'].unique()
    destination_communities = DATA['comunidad_destino'].unique()

    col3, col4 = st.columns(2)

    # Origin community analysis
    with col3:
        selected_community = st.selectbox("Select Origin Autonomous Community", origin_communities)
        community_data = DATA[DATA['comunidad_origen'] == selected_community]
        weekly_travelers_origin_community = community_data.groupby(['year', 'day_of_week'])['viajeros'].sum().reset_index()

        st.write(f"### Travelers by Day of the Week (Origin Community: {selected_community})")
        for year in years:
            st.write(f"#### {year}")
            year_data = weekly_travelers_origin_community[weekly_travelers_origin_community['year'] == year].set_index('day_of_week')
            st.line_chart(year_data[['viajeros']])

    # Destination community analysis
    with col4:
        selected_community_destino = st.selectbox("Select Destination Autonomous Community", destination_communities)
        community_data_destino = DATA[DATA['comunidad_destino'] == selected_community_destino]
        weekly_travelers_destino_community = community_data_destino.groupby(['year', 'day_of_week'])['viajeros'].sum().reset_index()

        st.write(f"### Travelers by Day of the Week (Destination Community: {selected_community_destino})")
        for year in years:
            st.write(f"#### {year}")
            year_data = weekly_travelers_destino_community[weekly_travelers_destino_community['year'] == year].set_index('day_of_week')
            st.line_chart(year_data[['viajeros']])

if __name__ == '__main__':
    main()
