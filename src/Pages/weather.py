import pandas as pd
import streamlit as st
from utils.helpers import df_capitals, DATA
import pydeck as pdk
from datetime import datetime
from data_analysis.plots import display_basic_weather_map, display_weather_with_color_transition


st.set_page_config(layout="wide")

st.header("NexMove: Mobility data at your fingertips", anchor=False, divider="red")
st.subheader("WEATHER")

st.subheader("TEMPERATURE ON SPECIFIC DAY")
df_weather = df_capitals

# Allow the user to select a date
selected_date = st.date_input("Select a date", value=datetime(2023, 9, 8))

# Create two columns for displaying the maps
col1, col2 = st.columns(2)

# Call the functions to display the maps inside the columns
with col1:
    st.write('## Minimum and Maximum Temperaturees of the day (put mouse on the province to see)')
    display_basic_weather_map(df_weather, selected_date)

with col2:
    st.write('## Average temperatures of the day from colder to warmer (blue - yellow - orange -red)')
    display_weather_with_color_transition(df_weather, selected_date)
    


st.write(df_capitals)










import altair as alt

df = DATA
st.write(df)

# Streamlit app setup
st.title("Travel and Weather Insights")
st.write("Analyze the relationship between weather and the number of travelers across provinces.")

# Filter options
province = st.selectbox("Select a province", df["provincia_destino_name"].unique())
year = st.selectbox("Select a year", df["year"].unique())
month = st.selectbox("Select a month", df["month"].unique())

# Filter travel data based on user selection
df_filtered_travel = df[
    (df["provincia_destino_name"] == province) &
    (df["year"] == year) &
    (df["month"] == month)
]

# Aggregate travelers for origin and destination by day
travel_origin = df_filtered_travel.groupby("day").agg({"viajeros": "sum"}).reset_index()
travel_destination = df_filtered_travel.groupby("day").agg({"viajes": "sum"}).reset_index()

# Filter weather data based on user selection
df_weather["day"] = pd.to_datetime(df_weather["day"])
df_filtered_weather = df_weather[
    (df_weather["desc_provincia"] == province) &
    (df_weather["day"].dt.year == year) &
    (df_weather["day"].dt.strftime("%B") == month)
]

# Merge weather data with travelers' data
merged_origin = pd.merge(travel_origin, df_filtered_weather, on="day", how="left")
merged_destination = pd.merge(travel_destination, df_filtered_weather, on="day", how="left")

# Function to create the Altair line chart
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

    # Conditional coloring for points
    points = base.mark_point(size=100).encode(
        color=alt.condition(
            alt.FieldOneOfPredicate("preciptype", ["snow"]),
            alt.value("white"),  # Snow points are white
            alt.condition(
                alt.FieldOneOfPredicate("preciptype", ["rain"]),
                alt.value("blue"),  # Rain points are blue
                alt.value("purple")  # Default points are purple
            )
        )
    )
    
    return (base + points).properties(title=title)

# Create line charts
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

# Display charts side by side
col1, col2 = st.columns(2)
with col1:
    st.altair_chart(origin_chart, use_container_width=True)
with col2:
    st.altair_chart(destination_chart, use_container_width=True)
