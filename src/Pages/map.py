import streamlit as st
import pandas as pd
import pydeck as pdk
from utils.helpers import DATA

st.set_page_config(layout="wide")

# Example: Coordinate data for provinces
coordinates_df = pd.DataFrame({
    #'provincia_origen_name': sorted(DATA['provincia_origen_name'].unique()),
    'provincia_origen_name': ['Albacete', 'Alicante', 'Almería'],
    'latitude': [38.9943, 38.3452, 36.8340],  # Example latitudes
    'longitude': [-1.8585, -0.4815, -2.4637]  # Example longitudes
})

# Group by province and calculate total travelers per province
province_data = DATA.groupby('provincia_origen_name')['viajeros'].sum().reset_index()
province_data.columns = ['provincia_origen_name', 'total_travelers']

# Merge coordinates with traveler data
province_data = pd.merge(province_data, coordinates_df, on='provincia_origen_name')

# Scale the radius of the dots based on the number of travelers
# (You may need to adjust the scaling factor for better visualization)
province_data['radius'] = province_data['total_travelers'] / 5000  # Adjust scaling as needed

# PyDeck map setup
st.write("## Interactive Map of Travelers by Province")
st.write("Provinces are displayed with larger circles based on the total number of travelers.")

# Define the PyDeck Layer for circles
layer = pdk.Layer(
    "ScatterplotLayer",
    data=province_data,
    get_position='[longitude, latitude]',
    get_radius="radius",  # Radius is proportional to the number of travelers
    get_fill_color="[200, 30, 0, 160]",  # Optional color customization
    pickable=True
)

# Set the view state to center over the geographic region
view_state = pdk.ViewState(
    latitude=40,  # Adjust to center of your region
    longitude=-3,
    zoom=5,
    pitch=0
)

# Render the deck.gl map in Streamlit
st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "{provincia_origen_name}: {total_travelers} travelers"}
))
