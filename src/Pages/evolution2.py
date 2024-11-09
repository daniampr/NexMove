import streamlit as st
import pandas as pd
import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from utils.helpers import DATA


DATA['day'] = pd.to_datetime(DATA['day'], errors='coerce')
DATA['month'] = DATA['day'].dt.month
DATA['year'] = DATA['day'].dt.year

# Get unique province names for the selection box
provinces = DATA['provincia_origen_name'].unique()

# Use columns to arrange layout horizontally
col1, col2 = st.columns([1, 5])  # Adjust the ratios as needed

with col1:
    st.write("## Number of Travelers per Month")  # Adjust title as needed

with col2:
    selected_province = st.selectbox("Select a Province", provinces)

# Filter data by the selected province
province_data = DATA[DATA['provincia_origen_name'] == selected_province]
monthly_travelers = province_data.groupby(['year', 'month'])['viajeros'].sum().reset_index()
years = monthly_travelers['year'].unique()

# Plotting each year
for year in years:
    st.write(f"Number of Travelers per Month in {year} with origin {selected_province}")
    year_data = monthly_travelers[monthly_travelers['year'] == year]
    year_data = year_data.set_index('month')
    st.line_chart(year_data[['viajeros']])