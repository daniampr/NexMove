# helper.py
import pandas as pd
import streamlit as st
import pydeck as pdk

# Coordinates for each province in Spain
province_coords = {
    "Alicante": [38.3452, -0.4810],
    "Almería": [36.8340, -2.4637],
    "Badajoz": [38.8794, -6.9706],
    "Islas Baleares": [39.6953, 3.0176],
    "Barcelona": [41.3851, 2.1734],
    "Burgos": [42.3439, -3.6969],
    "Cantabria": [43.1828, -3.9878],
    "Castellón": [39.9864, -0.0513],
    "Ciudad Real": [38.9848, -3.9272],
    "Cuenca": [40.0704, -2.1374],
    "Cáceres": [39.4755, -6.3723],
    "Cádiz": [36.5164, -6.2994],
    "Córdoba": [37.8882, -4.7794],
    "Gipuzkoa": [43.3128, -1.9750],
    "Girona": [41.9794, 2.8214],
    "Granada": [37.1773, -3.5986],
    "Guadalajara": [40.6293, -3.1628],
    "Huelva": [37.2614, -6.9447],
    "Jaén": [37.7796, -3.7849],
    "León": [42.5987, -5.5671],
    "Lugo": [43.0099, -7.5560],
    "Madrid": [40.4168, -3.7038],
    "Murcia": [37.9922, -1.1307],
    "Málaga": [36.7213, -4.4214],
    "Navarra": [42.6954, -1.6761],
    "Las Palmas": [28.1235, -15.4363],
    "Santa Cruz de Tenerife": [28.4636, -16.2518],
    "Segovia": [40.9429, -4.1088],
    "Sevilla": [37.3886, -5.9823],
    "Tarragona": [41.1189, 1.2445],
    "Teruel": [40.3440, -1.1069],
    "Toledo": [39.8628, -4.0273],
    "Valencia": [39.4699, -0.3763],
    "Zaragoza": [41.6488, -0.8891],
    "Albacete": [38.9943, -1.8564],
    "Álava": [42.8467, -2.6738],
    "Asturias": [43.3619, -5.8494],
    "Bizkaia": [43.2630, -2.9350],
    "A Coruña": [43.3623, -8.4115],
    "Huesca": [42.1401, -0.4089],
    "Lleida": [41.6176, 0.6200],
    "Pontevedra": [42.4300, -8.6444],
    "La Rioja": [42.2871, -2.5396],
    "Salamanca": [40.9701, -5.6635],
    "Soria": [41.7640, -2.4688],
    "Valladolid": [41.6523, -4.7245],
    "Ceuta": [35.8894, -5.3198],
    "Melilla": [35.2923, -2.9381],
    "Ourense": [42.3359, -7.8639],
    "Palencia": [42.0095, -4.5284],
    "Zamora": [41.5033, -5.7445],
    "Ávila": [40.6564, -4.6814]
}


# Map plotting function
def plot_map(data, tooltip_text, dot_size, average):
    
    # Aggregate total travelers by destination province
    if average == 'yes':
        province_data = data.groupby('provincia_destino_name')['viajeros'].mean().reset_index()
    else:
        province_data = data.groupby('provincia_destino_name')['viajeros'].sum().reset_index()

    province_data.columns = ['provincia_destino_name', 'total_travelers']
    province_data['formatted_travelers'] = province_data['total_travelers'].apply(lambda x: f"{x:,}")
    
    # Convert coordinates to a DataFrame and merge with province data
    coordinates_df = pd.DataFrame.from_dict(province_coords, orient='index', columns=['latitude', 'longitude']).reset_index()
    coordinates_df.columns = ['provincia_destino_name', 'latitude', 'longitude']
    
    # Merge province data with coordinates and compute the radius for each dot
    province_data = pd.merge(province_data, coordinates_df, on='provincia_destino_name')

    if dot_size == 'month':
        province_data['radius'] = province_data['total_travelers'] / 200  # Adjust radius scaling if needed
        zoom_ = 4.5
    elif dot_size == 'year':
        province_data['radius'] = province_data['total_travelers'] / 5000  # Adjust radius scaling if needed
        zoom_ = 5
    elif dot_size == 'day' and average == 'yes':
        province_data['radius'] = province_data['total_travelers'] * 10  # Adjust radius scaling if needed
        zoom_ = 4.5

    # Set up PyDeck layer
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=province_data,
        get_position='[longitude, latitude]',
        get_radius="radius",
        get_fill_color="[0, 128, 255, 160]",  # blue
        pickable=True
    )

    # View state of the map
    view_state = pdk.ViewState(
        latitude=40, 
        longitude=-3, 
        zoom=zoom_, 
        pitch=0
    )

    # Render the map
    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{provincia_destino_name}: {formatted_travelers} travelers"}
    ))
















##### weather



# Function to display the basic weather map (with fixed color for dots)
def display_basic_weather_map(df_weather, selected_date):
    # Filter the dataframe for the selected date
    df_weather['day'] = pd.to_datetime(df_weather['day'])
    filtered_data = df_weather[df_weather['day'] == pd.Timestamp(selected_date)]

    # Map province capitals to their coordinates
    filtered_data['coords'] = filtered_data['desc_provincia'].map(province_coords)

    # Drop rows without valid coordinates
    filtered_data = filtered_data.dropna(subset=['coords'])

    # Add latitude and longitude for PyDeck
    filtered_data['longitude'] = filtered_data['coords'].apply(lambda x: x[1])
    filtered_data['latitude'] = filtered_data['coords'].apply(lambda x: x[0])

    # PyDeck layer for temperatures (with fixed color)
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=filtered_data,
        get_position='[longitude, latitude]',
        get_radius=20000,  # Fixed radius for dots
        get_fill_color="[255, 255, 255, 255]", 
        pickable=True
    )

    # Map view configuration
    view_state = pdk.ViewState(
        latitude=40,
        longitude=-3,
        zoom=4.5,
        pitch=0
    )

    # Render map with a tooltip showing temperatures
    st.pydeck_chart(pdk.Deck(
        layers=[scatter_layer],
        initial_view_state=view_state,
        tooltip={"text": "Province: {desc_provincia}\nTemp Max: {tempmax}°C\nTemp Min: {tempmin}°C"}
    ))

# Function to display the weather map with color transitions based on temperature
def display_weather_with_color_transition(df_weather, selected_date):
    # Filter the dataframe for the selected date
    df_weather['day'] = pd.to_datetime(df_weather['day'])
    filtered_data = df_weather[df_weather['day'] == pd.Timestamp(selected_date)]

    # Map province capitals to their coordinates
    filtered_data['coords'] = filtered_data['desc_provincia'].map(province_coords)

    # Drop rows without valid coordinates
    filtered_data = filtered_data.dropna(subset=['coords'])

    # Add latitude and longitude for PyDeck
    filtered_data['longitude'] = filtered_data['coords'].apply(lambda x: x[1])
    filtered_data['latitude'] = filtered_data['coords'].apply(lambda x: x[0])

    # Calculate average temperature
    filtered_data['temp_avg'] = (filtered_data['temp'])

    # Define color transition formula based on temp_avg
    def get_color(temp):
        if temp <= 10:
            # Blue to Yellow transition
            return [0, int((temp / 10) * 255), 255, 160]
        elif temp <= 20:
            # Yellow to Orange transition
            return [int(((temp - 10) / 10) * 255), 255, 0, 160]
        else:
            # Orange to Red transition
            return [255, int((1 - (temp - 20) / 10) * 128), 0, 160]

    filtered_data['color'] = filtered_data['temp_avg'].apply(get_color)

    # PyDeck layer for temperatures with continuous color transitions
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=filtered_data,
        get_position='[longitude, latitude]',
        get_radius=20000,  # Fixed radius for dots
        get_fill_color='color',  # Dynamic color
        pickable=True
    )

    # Map view configuration
    view_state = pdk.ViewState(
        latitude=40,
        longitude=-3,
        zoom=4.5,
        pitch=0
    )

    # Render map with a tooltip showing temperatures
    st.pydeck_chart(pdk.Deck(
        layers=[scatter_layer],
        initial_view_state=view_state,
        tooltip={"text": "Province: {desc_provincia}\nTemp Avg: {temp_avg}°C"}
    ))
