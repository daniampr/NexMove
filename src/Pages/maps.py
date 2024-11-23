import streamlit as st
import pandas as pd
import pydeck as pdk
import base64  # Importing base64 for encoding images
from datetime import datetime
from utils.helpers import DATA
from data_analysis.plots import plot_map, province_coords


# Setup configuration and global CSS
def setup():
    st.set_page_config(
        page_title="Map Visualization",
        page_icon="🗺️",
        layout="wide",
    )

    # Function to encode image to base64
    def get_base64_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()

    # Background styling
    background_image = "starrynight_5.jpg"  # Path to your image file
    encoded_background = get_base64_image(background_image)

    # CSS Styling
    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background: url("data:image/jpg;base64,{encoded_background}") no-repeat center center fixed;
            background-size: cover;
            font-family: 'Poppins', sans-serif;
            color: #ffffff;  /* White text */
        }}
        .main-title {{
            text-align: center;
            font-size: 2.5rem;
            font-weight: bold;
            color: #ffffff;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
        }}
        .subtitle {{
            text-align: center;
            font-size: 1.5rem;
            color: #ffffff;
            margin-bottom: 20px;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
        }}
        .divider {{
            border-top: 3px solid #00aaff;
            margin: 20px 0;
        }}
        div[data-testid="stSelectbox"] > label {{
            color: #ffffff;
            font-size: 16px;
            font-weight: bold;
        }}
        div[data-testid="stHorizontalBlock"] {{
            display: flex;
            justify-content: center;
            align-items: flex-start;
            gap: 20px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# Main function
def main():
    setup()

    # Title and subtitle
    st.markdown("<h1 class='main-title'>Map Visualization</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='subtitle'>Interactive Maps with Data Insights</h2>", unsafe_allow_html=True)

    # Divider
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Map of total travelers by province of destination
    st.write("### Map of Total Travelers by Province of Destination")
    st.write("Provinces are displayed with larger circles based on the total number of travelers.")
    df_filtered = DATA[DATA['provincia_destino_name'].isin(province_coords.keys())]
    plot_map(df_filtered, "{provincia_destino_name}: {total_travelers} travelers", dot_size="year", average="no")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Month selection for total travelers per year
    st.write("### Select a Month to View Total Travelers per Province for Each Year (2022, 2023, 2024)")
    st.write("Dot size scaling may change as numbers vary across years.")
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month = st.selectbox("Select Month", options=month_order, index=8)

    # Filter data and create columns for years
    df_filtered = DATA[DATA['provincia_destino_name'].isin(province_coords.keys())]
    df_filtered = df_filtered[df_filtered['month'] == month]
    col2022, col2023, col2024 = st.columns(3)

    for col, year in zip([col2022, col2023, col2024], [2022, 2023, 2024]):
        with col:
            st.write(f"#### {year} - Total Travelers for {month}")
            year_data = df_filtered[df_filtered['year'] == year]
            if not year_data.empty:
                plot_map(year_data, f"{year} - {{provincia_destino_name}}: {{total_travelers}} travelers", dot_size="month", average="no")
            else:
                st.write(f"No data available for {year} in {month}.")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Top trips visualization
    st.write("### Top Trips")
    num_trips = st.selectbox(
        "Select the number of top trips to display",
        options=[5, 10, 15, 20, 25, 30, 40, 50],
        index=5,
    )

    DATA['trip_pair'] = DATA.apply(
        lambda x: '-'.join(sorted([x['provincia_origen_name'], x['provincia_destino_name']])), axis=1
    )
    top_trips = (
        DATA.groupby('trip_pair')['viajeros']
        .sum()
        .reset_index()
        .sort_values(by='viajeros', ascending=False)
        .head(num_trips)
    )
    top_trips[['origin', 'destination']] = top_trips['trip_pair'].str.split('-', expand=True)
    top_trips['origin_coords'] = top_trips['origin'].map(province_coords)
    top_trips['destination_coords'] = top_trips['destination'].map(province_coords)
    top_trips = top_trips.dropna(subset=['origin_coords', 'destination_coords'])

    # Prepare data for PyDeck
    top_trips['origin_longitude'] = top_trips['origin_coords'].apply(lambda x: x[1])
    top_trips['origin_latitude'] = top_trips['origin_coords'].apply(lambda x: x[0])
    top_trips['destination_longitude'] = top_trips['destination_coords'].apply(lambda x: x[1])
    top_trips['destination_latitude'] = top_trips['destination_coords'].apply(lambda x: x[0])

    line_layer = pdk.Layer(
        "LineLayer",
        data=top_trips,
        get_source_position='[origin_longitude, origin_latitude]',
        get_target_position='[destination_longitude, destination_latitude]',
        get_width='viajeros / 30000000',
        get_color=[0, 128, 255, 160],
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=40,
        longitude=-3,
        zoom=5,
        pitch=0,
    )

    st.pydeck_chart(pdk.Deck(
        layers=[line_layer],
        initial_view_state=view_state,
        tooltip={"text": "{origin} to {destination}: {viajeros} travelers"},
    ))

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Average number of travelers by day and month
    st.write("### Average Number of Travelers by Day and Month")
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day = st.selectbox("Select Day", options=day_order)

    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month = st.selectbox("Select Month", options=month_order)

    df_filtered = DATA[DATA['provincia_destino_name'].isin(province_coords.keys())]
    df_filtered = df_filtered[df_filtered['day_of_week'] == day]
    df_filtered = df_filtered[df_filtered['month'] == month]

    plot_map(df_filtered, "{provincia_destino_name}: {total_travelers} travelers", dot_size="day", average="yes")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Average number of travelers for a specific date
    st.write("### Average Number of Travelers for a Specific Date")
    selected_date = st.date_input("Select a date", value=datetime(2022, 9, 1))
    df_filtered = DATA[DATA['provincia_destino_name'].isin(province_coords.keys())]
    df_filtered = df_filtered[df_filtered['day'] == str(selected_date)]

    plot_map(df_filtered, "{provincia_destino_name}: {total_travelers} travelers", dot_size="day", average="yes")


if __name__ == "__main__":
    main()
