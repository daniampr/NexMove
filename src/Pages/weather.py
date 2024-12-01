import pandas as pd
import streamlit as st
from utils.helpers import df_capitals, DATA
import pydeck as pdk
from datetime import datetime
from data_analysis.plots import display_basic_weather_map, display_weather_with_color_transition, create_travel_chart
import altair as alt


# Function to encode image to base64
def get_base64_image(image_path):
    import base64
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


# Configuración inicial
def setup():

    # CSS Styling
    st.markdown(
        f"""
        <style>
        .header-title {{
            font-size: 2rem;
            font-weight: bold;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
            text-align: center;
        }}
        .header-subtitle {{
            font-size: 1.2rem;
            margin: 0;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
            text-align: center;
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
        div[data-testid="stDateInput"] > label,
        div[data-testid="stSelectbox"] > label {{
            color: #ffffff !important;  /* Label text color (e.g., 'Select a date', 'Select province') */
            font-size: 16px !important;
            font-weight: bold !important;
        }}
        div[data-testid="stDateInput"] input {{
            color: #000000 !important;  /* Ensure date text is black */
            background-color: transparent !important;  /* Keep background as default */
        }}
        div[data-baseweb="select"] > div {{
            background-color: #ffffff !important;  /* Keep dropdown box background white */
            color: #000000 !important;  /* Dropdown text remains black */
            border: 1px solid #00d2ff !important;  /* Optional blue border for consistency */
            border-radius: 5px !important;  /* Smooth corners */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# Main function
def weather_main():
    setup()

   # Header section
    st.markdown(
        """
        <h1 class="header-title">NexMove: Mobility and Weather Insights</h1>
        <p class="header-subtitle">Explore how weather and mobility intersect across regions</p>
        """,
        unsafe_allow_html=True
    )

    st.subheader("WEATHER")

    # Weather analysis
    st.subheader("TEMPERATURE ON SPECIFIC DAY")
    df_weather = df_capitals

    # Allow the user to select a date
    selected_date = st.date_input("Select a date", value=datetime(2023, 9, 8))

    # Create two columns for displaying the maps
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h3>Minimum and Maximum Temperatures of the day</h3>", unsafe_allow_html=True)
        display_basic_weather_map(df_weather, selected_date)

    with col2:
        st.markdown("<h3>Average Temperatures (Color Transition)</h3>", unsafe_allow_html=True)
        display_weather_with_color_transition(df_weather, selected_date)

    st.divider()

    # Travel analysis
    st.title("Travel and Weather Insights")
    st.write("Analyze the relationship between weather and the number of travelers across provinces.")

    # Filter options
    province = st.selectbox("Select a province", DATA["provincia_destino_name"].unique(), index=35)
    year = st.selectbox("Select a year", DATA["year"].unique(), index=1)
    month = st.selectbox("Select a month", DATA["month"].unique(), index=4)




    # Filter and aggregate data
    df_filtered_travel = DATA[
        (DATA["provincia_destino_name"] == province) &
        (DATA["year"] == year) &
        (DATA["month"] == month)
    ]

    travel_origin = df_filtered_travel.groupby("day").agg({"viajeros": "sum"}).reset_index()
    travel_destination = df_filtered_travel.groupby("day").agg({"viajes": "sum"}).reset_index()

    df_weather["day"] = pd.to_datetime(df_weather["day"])
    df_filtered_weather = df_weather[
        (df_weather["desc_provincia"] == province) &
        (df_weather["day"].dt.year == year) &
        (df_weather["day"].dt.strftime("%B") == month)
    ]

    # Merge weather with travel data
    # Ensure "day" is datetime in both DataFrames before merging
    travel_origin["day"] = pd.to_datetime(travel_origin["day"])
    travel_destination["day"] = pd.to_datetime(travel_destination["day"])

    # Merge weather with travel data
    merged_origin = pd.merge(travel_origin, df_filtered_weather, on="day", how="left")
    merged_destination = pd.merge(travel_destination, df_filtered_weather, on="day", how="left")



    #origin_chart = create_travel_chart(merged_origin.rename(columns={"viajes": "Travelers"}),  "Travelers",  f"Travelers to {province} (Origin)", "Rain")
    destination_chart = create_travel_chart(merged_destination.rename(columns={"viajes": "Travelers"}),  "Travelers",  f"Travelers to {province} (Destination)", "Rain") #"'rain'")
    st.altair_chart(destination_chart, use_container_width=True)
    st.write("Put mouse on any point to see the day, precipitation of that day, maximum and minimum temperatures, and number of travelers.")
