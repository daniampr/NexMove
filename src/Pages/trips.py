import streamlit as st 
import pandas as pd
from utils.helpers import DATA

st.set_page_config(layout="wide")

st.header("NexMove: Mobility data at your fingertips", anchor=False, divider="red")
st.subheader('INTERACTIVE DATA')

# Verify that the DataFrame DATA is loaded and contains the 'day' column
if 'day' in DATA.columns:
    # Convert the 'day' column to datetime format
    DATA['day'] = pd.to_datetime(DATA['day'], errors='coerce')
else:
    st.error("Error: The 'day' column is not found in the DataFrame DATA.")
    st.stop()  # Stop execution if the 'day' column does not exist

# Select Origin Province
st.write("### Select Origin Province for Mobility Analysis")
provinces = DATA['provincia_origen_name'].unique()  # Origin provinces
selected_province = st.selectbox("Select Province", provinces)

# Date inputs for selecting the time period, limited between 2022 and 2024 for origin province
st.write("### Select a Time Period for Origin Province")
start_date_origin_province = st.date_input("Start Date", value=pd.to_datetime("2022-01-01"), 
                                           min_value=pd.to_datetime("2022-01-01"), 
                                           max_value=pd.to_datetime("2024-12-31"), 
                                           key="start_date_origin_province")
end_date_origin_province = st.date_input("End Date", value=pd.to_datetime("2022-12-31"), 
                                         min_value=pd.to_datetime("2022-01-01"), 
                                         max_value=pd.to_datetime("2024-12-31"), 
                                         key="end_date_origin_province")

# Filter data based on the selected origin province and date range
filtered_data_origin_province = DATA[
    (DATA['provincia_origen_name'] == selected_province) &
    (DATA['day'] >= pd.to_datetime(start_date_origin_province)) &
    (DATA['day'] <= pd.to_datetime(end_date_origin_province))
]

# Check if there is data in the applied filter for the origin province
if not filtered_data_origin_province.empty:
    # Group by day and sum 'viajeros' column for the selected origin province and date range
    daily_travelers_origin_province = filtered_data_origin_province.groupby('day')['viajeros'].sum().reset_index()
    daily_travelers_origin_province['day'] = daily_travelers_origin_province['day'].dt.strftime('%Y-%m-%d')  # Convert date to string

    # Create bar chart with st.bar_chart
    st.write(f"## Mobility Data for {selected_province} (Origin) from {start_date_origin_province} to {end_date_origin_province}")
    daily_travelers_origin_province.set_index('day', inplace=True)
    st.bar_chart(daily_travelers_origin_province['viajeros'])
else:
    st.write("No data available for the selected origin province and date range.")

# Select Destination Province
st.write("### Select Destination Province for Mobility Analysis")
destination_provinces = DATA['provincia_destino_name'].unique()  # Destination provinces
selected_province_dest = st.selectbox("Select Destination Province", destination_provinces)

# Date inputs for selecting the time period, limited between 2022 and 2024 for destination province
st.write("### Select a Time Period for Destination Province")
start_date_dest_province = st.date_input("Start Date", value=pd.to_datetime("2022-01-01"), 
                                         min_value=pd.to_datetime("2022-01-01"), 
                                         max_value=pd.to_datetime("2024-12-31"), 
                                         key="start_date_dest_province")
end_date_dest_province = st.date_input("End Date", value=pd.to_datetime("2022-12-31"), 
                                       min_value=pd.to_datetime("2022-01-01"), 
                                       max_value=pd.to_datetime("2024-12-31"), 
                                       key="end_date_dest_province")

# Filter data based on the selected destination province and date range
filtered_data_dest_province = DATA[
    (DATA['provincia_destino_name'] == selected_province_dest) &
    (DATA['day'] >= pd.to_datetime(start_date_dest_province)) &
    (DATA['day'] <= pd.to_datetime(end_date_dest_province))
]

# Check if there is data in the applied filter for the destination province
if not filtered_data_dest_province.empty:
    # Group by day and sum 'viajeros' column for the selected destination province and date range
    daily_travelers_dest_province = filtered_data_dest_province.groupby('day')['viajeros'].sum().reset_index()
    daily_travelers_dest_province['day'] = daily_travelers_dest_province['day'].dt.strftime('%Y-%m-%d')  # Convert date to string

    # Create bar chart with st.bar_chart
    st.write(f"## Mobility Data for {selected_province_dest} (Destination) from {start_date_dest_province} to {end_date_dest_province}")
    daily_travelers_dest_province.set_index('day', inplace=True)
    st.bar_chart(daily_travelers_dest_province['viajeros'])
else:
    st.write("No data available for the selected destination province and date range.")

# Select Origin Autonomous Community
st.write("### Select Origin Autonomous Community for Mobility Analysis")
origin_communities = DATA['comunidad_origen'].unique()  # Origin autonomous communities
selected_origin_community = st.selectbox("Select Origin Autonomous Community", origin_communities)

# Date inputs to select the time period, limited between 2022 and 2024 for origin autonomous community
st.write("### Select a Time Period for Origin Autonomous Community")
start_date_origin_community = st.date_input("Start Date", value=pd.to_datetime("2022-01-01"), 
                                            min_value=pd.to_datetime("2022-01-01"), 
                                            max_value=pd.to_datetime("2024-12-31"), 
                                            key="start_date_origin_community")
end_date_origin_community = st.date_input("End Date", value=pd.to_datetime("2022-12-31"), 
                                          min_value=pd.to_datetime("2022-01-01"), 
                                          max_value=pd.to_datetime("2024-12-31"), 
                                          key="end_date_origin_community")

# Filter data based on the selected origin autonomous community and date range
filtered_data_origin_community = DATA[
    (DATA['comunidad_origen'] == selected_origin_community) &
    (DATA['day'] >= pd.to_datetime(start_date_origin_community)) &
    (DATA['day'] <= pd.to_datetime(end_date_origin_community))
]

# Check if there is data in the applied filter for the origin autonomous community
if not filtered_data_origin_community.empty:
    # Group by day and sum 'viajeros' column for the selected origin autonomous community and date range
    daily_travelers_origin_community = filtered_data_origin_community.groupby('day')['viajeros'].sum().reset_index()
    daily_travelers_origin_community['day'] = daily_travelers_origin_community['day'].dt.strftime('%Y-%m-%d')  # Convert date to string

    # Create bar chart with st.bar_chart
    st.write(f"## Mobility Data for {selected_origin_community} (Origin) from {start_date_origin_community} to {end_date_origin_community}")
    daily_travelers_origin_community.set_index('day', inplace=True)
    st.bar_chart(daily_travelers_origin_community['viajeros'])
else:
    st.write("No data available for the selected origin autonomous community and date range.")

# Select Destination Autonomous Community
st.write("### Select Destination Autonomous Community for Mobility Analysis")
destination_communities = DATA['comunidad_destino'].unique()  # Destination autonomous communities
selected_destination_community = st.selectbox("Select Destination Autonomous Community", destination_communities)

# Date inputs to select the time period, limited between 2022 and 2024 for destination autonomous community
st.write("### Select a Time Period for Destination Autonomous Community")
start_date_dest_community = st.date_input("Start Date", value=pd.to_datetime("2022-01-01"), 
                                          min_value=pd.to_datetime("2022-01-01"), 
                                          max_value=pd.to_datetime("2024-12-31"), 
                                          key="start_date_dest_community")
end_date_dest_community = st.date_input("End Date", value=pd.to_datetime("2022-12-31"), 
                                        min_value=pd.to_datetime("2022-01-01"), 
                                        max_value=pd.to_datetime("2024-12-31"), 
                                        key="end_date_dest_community")

# Filter data based on the selected destination autonomous community and date range
filtered_data_dest_community = DATA[
    (DATA['comunidad_destino'] == selected_destination_community) &
    (DATA['day'] >= pd.to_datetime(start_date_dest_community)) &
    (DATA['day'] <= pd.to_datetime(end_date_dest_community))
]

# Check if there is data in the applied filter for the destination autonomous community
if not filtered_data_dest_community.empty:
    # Group by day and sum 'viajeros' column for the selected destination autonomous community and date range
    daily_travelers_dest_community = filtered_data_dest_community.groupby('day')['viajeros'].sum().reset_index()
    daily_travelers_dest_community['day'] = daily_travelers_dest_community['day'].dt.strftime('%Y-%m-%d')  # Convert date to string

    # Create the bar chart with st.bar_chart
    st.write(f"## Mobility Data for {selected_destination_community} (Destination) from {start_date_dest_community} to {end_date_dest_community}")
    daily_travelers_dest_community.set_index('day', inplace=True)  # Set 'day' as index for the chart
    st.bar_chart(daily_travelers_dest_community['viajeros'])  # Display bar chart
else:
    st.write("No data available for the selected destination autonomous community and date range.")