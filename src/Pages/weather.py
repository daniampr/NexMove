import pandas as pd
import streamlit as st
from utils.helpers import df_capitals, DATA
import pydeck as pdk
from datetime import datetime
from data_analysis.plots import display_basic_weather_map, display_weather_with_color_transition
import altair as alt

# Function to encode image to base64
def get_base64_image(image_path):
    import base64
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Configuración inicial
def setup():
    st.set_page_config(
        page_title="NexMove: Travel and Weather Insights",
        page_icon="🌡️",  # Thermometer icon
        layout="wide",
    )

    # Convert background image to base64
    background_image = get_base64_image("9_wallpaper.jpg")

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
def main():
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
    province = st.selectbox("Select a province", DATA["provincia_destino_name"].unique())
    year = st.selectbox("Select a year", DATA["year"].unique())
    month = st.selectbox("Select a month", DATA["month"].unique())

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
    merged_origin = pd.merge(travel_origin, df_filtered_weather, on="day", how="left")
    merged_destination = pd.merge(travel_destination, df_filtered_weather, on="day", how="left")

    # Function to create Altair chart
    def create_travel_chart(df, y_field, title):
        base = alt.Chart(df).mark_line(color="purple", point=True).encode(
            x=alt.X("day:T", title="Day of the Month"),
            y=alt.Y(f"{y_field}:Q", title="Number of Travelers"),
            tooltip=[
                alt.Tooltip("day:T", title="Date"),
                alt.Tooltip("preciptype:N", title="Precipitation Type"),
                alt.Tooltip("tempmax:Q", title="Max Temp (°C)"),
                alt.Tooltip("tempmin:Q", title="Min Temp (°C)"),
                alt.Tooltip(f"{y_field}:Q", title="Travelers"),
            ]
        )
        points = base.mark_point(size=100).encode(
            color=alt.condition(
                alt.FieldOneOfPredicate("preciptype", ["snow"]),
                alt.value("white"),
                alt.condition(
                    alt.FieldOneOfPredicate("preciptype", ["rain"]),
                    alt.value("blue"),
                    alt.value("purple")
                )
            )
        )
        return (base + points).properties(title=title)

    origin_chart = create_travel_chart(
        merged_origin.rename(columns={"viajeros": "Travelers"}), 
        "Travelers", 
        f"Travelers to {province} (Origin)"
    )

    destination_chart = create_travel_chart(
        merged_destination.rename(columns={"viajes": "Travelers"}), 
        "Travelers", 
        f"Travelers to {province} (Destination)"
    )

    # Display charts
    col3, col4 = st.columns(2)
    with col3:
        st.altair_chart(origin_chart, use_container_width=True)
    with col4:
        st.altair_chart(destination_chart, use_container_width=True)

if __name__ == '__main__':
    main()
