import streamlit as st
import pydeck as pdk
from datetime import datetime
from utils.helpers import load_dataset_main, setup_headers
from data_analysis.plots import plot_map, province_coords


# Main function
def maps_main():
    DATA = load_dataset_main()
    setup_headers()

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
