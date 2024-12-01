import streamlit as st
import pandas as pd
from utils.helpers import DATA, get_base64_image


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
def evolution_days_main():
    setup()

    # Main Title
    st.markdown("<h2 class='header-title'>INTERACTIVE DATA: EVOLUTION BY DAY OF THE WEEK</h2>", unsafe_allow_html=True)

    # Divider
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Ensure 'day_of_week' is properly categorized
    day_of_week_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    DATA['day_of_week'] = pd.Categorical(DATA['day_of_week'], categories=day_of_week_order, ordered=True)

    # Aggregate travelers by year and day of the week
    weekly_travelers = DATA.groupby(['year', 'day_of_week'])['viajeros'].sum().reset_index()

    # Create a pivot table with 'day_of_week' as rows and years as columns
    pivoted_data = weekly_travelers.pivot(index='day_of_week', columns='year', values='viajeros')

    # Combined chart for all years
    st.write("<h3 style='text-align: center;'>Total Number of Travelers per Day of the Week (Comparison by Year)</h3>", unsafe_allow_html=True)
    st.line_chart(pivoted_data)

    # Individual charts for each year
    years = weekly_travelers['year'].unique()
    cols = st.columns(len(years))

    for i, year in enumerate(years):
        with cols[i]:
            st.markdown(f"<h4 style='text-align: center;'>Travelers in {year}</h4>", unsafe_allow_html=True)
            year_data = weekly_travelers[weekly_travelers['year'] == year].set_index('day_of_week')
            st.line_chart(year_data[['viajeros']])

    st.divider()

    # Province-level insights
    st.write("<h3 style='text-align: center;'>Insights for Each Province (Origin & Destination)</h3>", unsafe_allow_html=True)

    origin_provinces = DATA['provincia_origen_name'].unique()
    destination_provinces = DATA['provincia_destino_name'].unique()

    col1, col2 = st.columns(2)

    with col1:
        selected_province = st.selectbox("Select Origin Province", origin_provinces)
        province_data = DATA[DATA['provincia_origen_name'] == selected_province]
        weekly_travelers_origin = province_data.groupby(['year', 'day_of_week'])['viajeros'].sum().reset_index()
        st.write(f"<h4 style='text-align: center;'>Travelers by Day of the Week (Origin: {selected_province})</h4>", unsafe_allow_html=True)
        for year in years:
            year_data = weekly_travelers_origin[weekly_travelers_origin['year'] == year].set_index('day_of_week')
            st.line_chart(year_data[['viajeros']])

    with col2:
        selected_province_destino = st.selectbox("Select Destination Province", destination_provinces)
        province_data_destino = DATA[DATA['provincia_destino_name'] == selected_province_destino]
        weekly_travelers_destino = province_data_destino.groupby(['year', 'day_of_week'])['viajeros'].sum().reset_index()
        st.write(f"<h4 style='text-align: center;'>Travelers by Day of the Week (Destination: {selected_province_destino})</h4>", unsafe_allow_html=True)
        for year in years:
            year_data = weekly_travelers_destino[weekly_travelers_destino['year'] == year].set_index('day_of_week')
            st.line_chart(year_data[['viajeros']])

    st.divider()

    # Autonomous community insights
    st.write("<h3 style='text-align: center;'>Insights for Each Autonomous Community (Origin & Destination)</h3>", unsafe_allow_html=True)

    origin_communities = DATA['comunidad_origen'].unique()
    destination_communities = DATA['comunidad_destino'].unique()

    col3, col4 = st.columns(2)

    with col3:
        selected_community = st.selectbox("Select Origin Autonomous Community", origin_communities)
        community_data = DATA[DATA['comunidad_origen'] == selected_community]
        weekly_travelers_origin_community = community_data.groupby(['year', 'day_of_week'])['viajeros'].sum().reset_index()
        st.write(f"<h4 style='text-align: center;'>Travelers by Day of the Week (Origin Community: {selected_community})</h4>", unsafe_allow_html=True)
        for year in years:
            year_data = weekly_travelers_origin_community[weekly_travelers_origin_community['year'] == year].set_index('day_of_week')
            st.line_chart(year_data[['viajeros']])

    with col4:
        selected_community_destino = st.selectbox("Select Destination Autonomous Community", destination_communities)
        community_data_destino = DATA[DATA['comunidad_destino'] == selected_community_destino]
        weekly_travelers_destino_community = community_data_destino.groupby(['year', 'day_of_week'])['viajeros'].sum().reset_index()
        st.write(f"<h4 style='text-align: center;'>Travelers by Day of the Week (Destination Community: {selected_community_destino})</h4>", unsafe_allow_html=True)
        for year in years:
            year_data = weekly_travelers_destino_community[weekly_travelers_destino_community['year'] == year].set_index('day_of_week')
            st.line_chart(year_data[['viajeros']])

