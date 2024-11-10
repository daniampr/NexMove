import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
from utils.helpers import DATA

st.set_page_config(layout="wide")


# Sample dataset (replace with your actual data)
coordinates_df = pd.DataFrame({
    'provincia_origen_name': ['Albacete', 'Alicante', 'Almería'],
    'latitude': [38.9943, 38.3452, 36.8340],
    'longitude': [-1.8585, -0.4815, -2.4637]
})


# Sum travelers per province
province_data = DATA.groupby('provincia_origen_name')['viajeros'].sum().reset_index()
province_data.columns = ['provincia_origen_name', 'total_travelers']
province_data = pd.merge(province_data, coordinates_df, on='provincia_origen_name')
province_data['radius'] = province_data['total_travelers'] / 5000

# Set up the PyDeck map
st.write("## Select a Province from the Map to See Monthly Travel Trends")
layer = pdk.Layer(
    "ScatterplotLayer",
    data=province_data,
    get_position='[longitude, latitude]',
    get_radius="radius",
    get_fill_color="[200, 30, 0, 160]",
    pickable=True
)

# Initial view state of the map
view_state = pdk.ViewState(
    latitude=40,
    longitude=-3,
    zoom=5,
    pitch=0
)

# Render the PyDeck map
map_click = st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "{provincia_origen_name}: {total_travelers} travelers"}
))

# Province selection logic
selected_province = st.selectbox(
    "Or choose a province directly:",
    options=province_data['provincia_origen_name'].unique()
)

# Display monthly travel trends for the selected province
st.write(f"### Monthly Travelers for {selected_province}")

# Filter data for the selected province
province_monthly_data = DATA[DATA['provincia_origen_name'] == selected_province]

# Plot the monthly trends per year
fig, ax = plt.subplots(figsize=(10, 6))

for year in province_monthly_data['year'].unique():
    yearly_data = province_monthly_data[province_monthly_data['year'] == year]
    ax.plot(yearly_data['month'], yearly_data['viajeros'], label=f"Year {year}")

ax.set_title(f"Monthly Travelers for {selected_province}")
ax.set_xlabel("Month")
ax.set_ylabel("Number of Travelers")
ax.legend()
st.pyplot(fig)
