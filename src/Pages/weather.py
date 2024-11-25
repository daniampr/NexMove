import pandas as pd
import streamlit as st
from utils.helpers import df_capitals, DATA
import pydeck as pdk
from datetime import datetime
import altair as alt
from data_analysis.plots import display_basic_weather_map, display_weather_with_color_transition, create_travel_chart


st.set_page_config(layout="wide")

st.header("NexMove: Mobility data at your fingertips", anchor=False, divider="red")
st.subheader("WEATHER")

st.subheader("TEMPERATURE ON SPECIFIC DAY")
df_weather = df_capitals

# Allow the user to select a date
selected_date = st.date_input("Select a date", value=datetime(2023, 1, 31))

# Create two columns for displaying the maps
col1, col2 = st.columns(2)

# Call the functions to display the maps inside the columns
with col1:
    st.write('## Minimum and Maximum Temperaturees of the day (put mouse on the province to see)')
    display_basic_weather_map(df_weather, selected_date)

with col2:
    st.write('## Average temperatures of the day from colder to warmer (blue - yellow - orange -red)')
    display_weather_with_color_transition(df_weather, selected_date)
    





df = DATA
#st.write(df)

# Streamlit app setup
st.title("Travel and Weather Insights")
st.write("Analyze the relationship between weather and the number of travelers across provinces.")

# Filter options
province = st.selectbox("Select a province", df["provincia_destino_name"].unique(), index=35)
year = st.selectbox("Select a year", df["year"].unique(), index=2)
month = st.selectbox("Select a month", df["month"].unique(), index=4)

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

# Ensure the 'day' column in travel_origin and travel_destination is in datetime format
travel_origin["day"] = pd.to_datetime(travel_origin["day"])
travel_destination["day"] = pd.to_datetime(travel_destination["day"])

# Merge weather data with travelers' data
merged_origin = pd.merge(travel_origin, df_filtered_weather, on="day", how="left")
merged_destination = pd.merge(travel_destination, df_filtered_weather, on="day", how="left")

# Ensure `day_of_week` is available in the merged data
merged_origin["day_of_week"] = merged_origin["day"].dt.day_name()
merged_destination["day_of_week"] = merged_destination["day"].dt.day_name()

# Clean the 'preciptype' column in both merged datasets
def clean_preciptype(value):
    if isinstance(value, str):
        return value.strip("[]").lower()  # Remove brackets and convert to lowercase
    return None

merged_origin["preciptype"] = merged_origin["preciptype"].apply(clean_preciptype)
merged_destination["preciptype"] = merged_destination["preciptype"].apply(clean_preciptype)






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



# Create line charts
origin_chart = create_travel_chart(
    merged_origin.rename(columns={"viajeros": "Travelers"}), 
    "Travelers", 
    f"Travelers to {province} (Origin)",
    precip_type_to_show="'rain'"
)

destination_chart = create_travel_chart(
    merged_destination.rename(columns={"viajes": "Travelers"}), 
    "Travelers", 
    f"Travelers to {province} (Destination)",
    precip_type_to_show="'rain'"
)

st.write("Displaying white points for rain. Put mouse on each point to see information of the day")
# Display charts side by side
col1, col2 = st.columns(2)
with col1:
    st.altair_chart(origin_chart, use_container_width=True)
with col2:
    st.altair_chart(destination_chart, use_container_width=True)


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


st.write("Displaying white points for snow. Put mouse on each point to see information of the day")
# Display charts side by side
col1, col2 = st.columns(2)
with col1:
    st.altair_chart(origin_chart, use_container_width=True)
with col2:
    st.altair_chart(destination_chart, use_container_width=True)




