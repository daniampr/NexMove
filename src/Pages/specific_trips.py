import streamlit as st
import pandas as pd
from utils.helpers import DATA

st.set_page_config(layout="wide")

st.header("NexMove: Mobility data at your fingertips", anchor=False, divider="red")
st.subheader("INTERACTIVE DATA: SPECIFIC TRIP ANALYSIS")

# Convert 'day' column to datetime format
DATA['day'] = pd.to_datetime(DATA['day'], errors='coerce')

# Select the year and month
st.write("## Select a Year and Month for Analysis")
selected_year = st.selectbox("Year", sorted(DATA['year'].unique()))
selected_month = st.selectbox("Month", sorted(DATA['month'].unique()))

# Filter data for the selected month and year
filtered_month_data = DATA[(DATA['year'] == selected_year) & (DATA['month'] == selected_month)]

# Trip Selection: Origin and Destination Provinces
st.write("## Select Origin and Destination Provinces for the Trip")

# Unique provinces for origin and destination
origin_provinces = sorted(filtered_month_data['provincia_origen_name'].unique())
destination_provinces = sorted(filtered_month_data['provincia_destino_name'].unique())

# User selection for origin and destination provinces
selected_origin_province = st.selectbox("Select Origin Province", origin_provinces)
selected_destination_province = st.selectbox("Select Destination Province", destination_provinces)

# Filter data for the selected origin and destination provinces
filtered_trip_data_provinces = filtered_month_data[
    (filtered_month_data['provincia_origen_name'] == selected_origin_province) &
    (filtered_month_data['provincia_destino_name'] == selected_destination_province)
]

# Display the line charts for provinces side by side
if not filtered_trip_data_provinces.empty:
    st.write(f"### Number of Travelers for Trip: {selected_origin_province} to {selected_destination_province} on {selected_month}, {selected_year}")

    # Create two columns for displaying the charts side by side
    col1, col2 = st.columns(2)

    with col1:
        # Line chart by Day of the Week (Provinces)
        travelers_by_day_of_week = (
            filtered_trip_data_provinces.groupby('day_of_week')['viajeros']
            .sum()
        )
        st.write("#### Travelers by Day of the Week (Provinces)")
        st.line_chart(travelers_by_day_of_week, height=300, use_container_width=True)

    with col2:
        # Line chart by Day of the Month (Provinces)
        travelers_by_day_of_month = filtered_trip_data_provinces.groupby('day_number')['viajeros'].sum().sort_index()
        st.write("#### Travelers by Day of the Month (Provinces)")
        st.line_chart(travelers_by_day_of_month, height=300, use_container_width=True)
else:
    st.write("No data available for the selected origin, destination, and date range for Provinces.")

# Now for Communities
st.write("## Select Origin and Destination Communities for the Trip")

# Unique communities for origin and destination
origin_communities = sorted(filtered_month_data['comunidad_origen'].unique())
destination_communities = sorted(filtered_month_data['comunidad_destino'].unique())

# User selection for origin and destination communities
selected_origin_community = st.selectbox("Select Origin Community", origin_communities)
selected_destination_community = st.selectbox("Select Destination Community", destination_communities)

# Filter data for the selected origin and destination communities
filtered_trip_data_communities = filtered_month_data[
    (filtered_month_data['comunidad_origen'] == selected_origin_community) &
    (filtered_month_data['comunidad_destino'] == selected_destination_community)
]

# Display the line charts for communities side by side
if not filtered_trip_data_communities.empty:
    st.write(f"### Number of Travelers for Trip: {selected_origin_community} to {selected_destination_community} on {selected_month}, {selected_year}")

    # Create two columns for displaying the charts side by side
    col1, col2 = st.columns(2)

    with col1:
        # Line chart by Day of the Week (Communities)
        travelers_by_day_of_week_communities = (
            filtered_trip_data_communities.groupby('day_of_week')['viajeros']
            .sum()
        )
        st.write("#### Travelers by Day of the Week (Communities)")
        st.line_chart(travelers_by_day_of_week_communities, height=300, use_container_width=True)

    with col2:
        # Line chart by Day of the Month (Communities)
        travelers_by_day_of_month_communities = filtered_trip_data_communities.groupby('day_number')['viajeros'].sum().sort_index()
        st.write("#### Travelers by Day of the Month (Communities)")
        st.line_chart(travelers_by_day_of_month_communities, height=300, use_container_width=True)
else:
    st.write("No data available for the selected origin, destination, and date range for Communities.")
