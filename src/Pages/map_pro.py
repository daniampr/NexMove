import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
from utils.helpers import DATA
from data_analysis.plots import plot_map, province_coords

st.set_page_config(layout="wide")

st.title("MAP VISUALIZATION")

st.write("# Map of Total Travelers by Province Of Destination")
st.write("Provinces are displayed with larger circles based on the total number of travelers.")

df_filtered = DATA[DATA['provincia_destino_name'].isin(province_coords.keys())]
plot_map(df_filtered, "{provincia_destino_name}: {total_travelers} travelers", dot_size = 'year')




############################################################################################################3




st.write("## Select a Month to View Total Travelers per Province for Each Year (2022, 2023, 2024)")
st.write("### Note that dot size scaling may change as now they are much smaller numbers")

month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
month = st.selectbox("Select Month", options=month_order)

# Filter the dataset for the selected month
df_filtered = DATA[DATA['provincia_destino_name'].isin(province_coords.keys())]
df_filtered = df_filtered[df_filtered['month'] == month]

col2022, col2023, col2024 = st.columns(3)

# Loop over each year and plot in the respective column
for col, year in zip([col2022, col2023, col2024], [2022, 2023, 2024]):
    with col:
        st.write(f"### {year} - Total Travelers for {month}")
        
        # Filter data for the current year
        year_data = df_filtered[df_filtered['year'] == year]
        
        # Check if year_data is empty
        if not year_data.empty:
            # Call the plot function for the filtered data in the selected column
            plot_map(year_data, f"{year} - {{provincia_destino_name}}: {{total_travelers}} travelers", dot_size='month')
        else:
            st.write(f"No data available for {year} in {month}.")





###########################################################################################################

st.write("## Select a Day of the Week")
st.write("### Note that dot size scaling may change as now they are much smaller numbers")

day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day = st.selectbox("Select Day", options=day_order)

# Filter the dataset for the selected month
df_filtered = DATA[DATA['provincia_destino_name'].isin(province_coords.keys())]
df_filtered = df_filtered[df_filtered['day_of_week'] == day]

plot_map(df_filtered, "{provincia_destino_name}: {total_travelers} travelers", dot_size = 'day')


############################################################################################################

#day = st.selectbox("Select Day", options={1,})


st.write('## Top 25 Trips')


# Standardize trip pairs and aggregate data
DATA['trip_pair'] = DATA.apply(
    lambda x: '-'.join(sorted([x['provincia_origen_name'], x['provincia_destino_name']])), axis=1
)
top_trips = (
    DATA.groupby('trip_pair')['viajeros']
    .sum()
    .reset_index()
    .sort_values(by='viajeros', ascending=False)
    .head(25)
)

# Split standardized pairs back into origin and destination for coordinate mapping
top_trips[['origin', 'destination']] = top_trips['trip_pair'].str.split('-', expand=True)

# Add coordinates for origin and destination provinces
top_trips['origin_coords'] = top_trips['origin'].map(province_coords)
top_trips['destination_coords'] = top_trips['destination'].map(province_coords)

# Remove any trips without valid coordinates
top_trips = top_trips.dropna(subset=['origin_coords', 'destination_coords'])

# Prepare the data for the LineLayer
top_trips['origin_longitude'] = top_trips['origin_coords'].apply(lambda x: x[1])
top_trips['origin_latitude'] = top_trips['origin_coords'].apply(lambda x: x[0])
top_trips['destination_longitude'] = top_trips['destination_coords'].apply(lambda x: x[1])
top_trips['destination_latitude'] = top_trips['destination_coords'].apply(lambda x: x[0])

# PyDeck layer for the top trips as lines with reduced thickness
line_layer = pdk.Layer(
    "LineLayer",
    data=top_trips,
    get_source_position='[origin_longitude, origin_latitude]',
    get_target_position='[destination_longitude, destination_latitude]',
    get_width='viajeros / 30000000',  # Reduced line width for thinner lines
    get_color=[0, 128, 255, 160],  # Red color for lines
    pickable=True
)

# Set up the PyDeck view state
view_state = pdk.ViewState(
    latitude=40,
    longitude=-3,
    zoom=5,
    pitch=0
)

# Render the map with both scatterplot and line layers
st.pydeck_chart(pdk.Deck(
    layers=[
        line_layer,  # Layer for top 10 trip lines
    ],
    initial_view_state=view_state,
    tooltip={"text": "{origin} to {destination}: {viajeros} travelers"}
))

























