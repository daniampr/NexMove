import streamlit as st
import numpy as np
import pandas as pd
from utils.helpers import setup_headers, load_dataset_main


# Main function
def evolution_months_main():
    DATA = load_dataset_main()
    setup_headers()

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
