import pandas as pd
import streamlit as st
from utils.helpers import df_capitals
import pydeck as pdk
from datetime import datetime
from data_analysis.plots import display_basic_weather_map, display_weather_with_color_transition



st.set_page_config(layout="wide")

st.header("NexMove: Mobility data at your fingertips", anchor=False, divider="red")
st.subheader("WEATHER CONDITIONS")


# Display the filtered DataFrame
st.write(df_capitals)
df_weather = df_capitals

# Allow the user to select a date
selected_date = st.date_input("Select a date", value=datetime(2023, 8, 8))

# Create two columns for displaying the maps
col1, col2 = st.columns(2)

# Call the functions to display the maps inside the columns
with col1:
    st.write('## Minimum and Maximum Temperaturees of the day (put mouse on the province to see)')
    display_basic_weather_map(df_weather, selected_date)

with col2:
    st.write('## Average temperatures of the day from colder to warmer (blue - yellow - orange -red)')
    display_weather_with_color_transition(df_weather, selected_date)
