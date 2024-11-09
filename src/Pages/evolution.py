import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from utils.helpers import DATA

st.set_page_config(layout="wide")

st.header("NexMove: Mobility data at your fingertips", anchor=False, divider="red")
st.subheader('INTERACTIVE DATA')

# Ensure 'day' column is in datetime format
DATA['day'] = pd.to_datetime(DATA['day'], errors='coerce')

# Group by year and month, then sum the 'viajeros' column
monthly_travelers = DATA.groupby(['year', 'month'])['viajeros'].sum().reset_index()

# Pivot the data so that 'month' is the index, and each column is a year
pivoted_data = monthly_travelers.pivot(index='month', columns='year', values='viajeros')

# 1. Display the combined plot of all years
st.write("## Total Number of Travelers per Month (Comparison by Year)")
st.line_chart(pivoted_data)

# 2. Display individual year plots side-by-side
years = monthly_travelers['year'].unique()
cols = st.columns(len(years))  # Create a column for each year

for i, year in enumerate(years):
    with cols[i]:  # Use each column for one year
        st.write(f"### Total Travelers per Month in {year}")
        year_data = monthly_travelers[monthly_travelers['year'] == year].set_index('month')
        st.line_chart(year_data[['viajeros']])

# Add the title for province insights
st.write("## Insights for each province (origin & destination)")

# 3. Layout for province selections and their respective plots
# Get unique provinces for origin and destination
origin_provinces = DATA['provincia_origen_name'].unique()
destination_provinces = DATA['provincia_destino_name'].unique()

col1, col2 = st.columns(2)  # Create two columns for origin and destination

# Origin Province Selection and Plot
with col1:
    selected_province = st.selectbox("Select Origin Province", origin_provinces)
    province_data = DATA[DATA['provincia_origen_name'] == selected_province]
    monthly_travelers_origin = province_data.groupby(['year', 'month'])['viajeros'].sum().reset_index()
    
    st.write(f"### Travelers per Month (Origin: {selected_province})")
    
    # Plot each year's data separately for the selected origin province
    for year in years:
        st.write(f"#### {year}")
        year_data = monthly_travelers_origin[monthly_travelers_origin['year'] == year].set_index('month')
        st.line_chart(year_data[['viajeros']])

# Destination Province Selection and Plot
with col2:
    selected_province_destino = st.selectbox("Select Destination Province", destination_provinces)
    province_data_destino = DATA[DATA['provincia_destino_name'] == selected_province_destino]
    monthly_travelers_destino = province_data_destino.groupby(['year', 'month'])['viajeros'].sum().reset_index()
    
    st.write(f"### Travelers per Month (Destination: {selected_province_destino})")
    
    # Plot each year's data separately for the selected destination province
    for year in years:
        st.write(f"#### {year}")
        year_data = monthly_travelers_destino[monthly_travelers_destino['year'] == year].set_index('month')
        st.line_chart(year_data[['viajeros']])

# Add the title for community insights
st.write("## Insights for each Autonomous Community (origin & destination)")

# 4. Layout for community selections and their respective plots
# Get unique communities for origin and destination
origin_communities = DATA['comunidad_origen'].unique()
destination_communities = DATA['comunidad_destino'].unique()

col3, col4 = st.columns(2)  # Create two columns for origin and destination community

# Origin Community Selection and Plot
with col3:
    selected_community = st.selectbox("Select Origin Autonomous Community", origin_communities)
    community_data = DATA[DATA['comunidad_origen'] == selected_community]
    monthly_travelers_origin_community = community_data.groupby(['year', 'month'])['viajeros'].sum().reset_index()
    
    st.write(f"### Travelers per Month (Origin Community: {selected_community})")
    # Plot each year's data separately for the selected origin community
    for year in years:
        st.write(f"#### {year}")
        year_data = monthly_travelers_origin_community[monthly_travelers_origin_community['year'] == year].set_index('month')
        st.line_chart(year_data[['viajeros']])

# Destination Community Selection and Plot
with col4:
    selected_community_destino = st.selectbox("Select Destination Autonomous Community", destination_communities)
    community_data_destino = DATA[DATA['comunidad_destino'] == selected_community_destino]
    monthly_travelers_destino_community = community_data_destino.groupby(['year', 'month'])['viajeros'].sum().reset_index()
    
    st.write(f"### Travelers per Month (Destination Community: {selected_community_destino})")
    # Plot each year's data separately for the selected destination community
    for year in years:
        st.write(f"#### {year}")
        year_data = monthly_travelers_destino_community[monthly_travelers_destino_community['year'] == year].set_index('month')
        st.line_chart(year_data[['viajeros']])
