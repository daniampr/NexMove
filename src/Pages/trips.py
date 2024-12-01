import streamlit as st
import pandas as pd
import base64  # For encoding the background image
from utils.helpers import DATA


# Setup configuration and global CSS
def setup():
    # CSS Styling
    st.markdown(
        f"""
        <style>
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
def trips_main():
    setup()

    # Title and subtitle
    st.markdown("<h1 class='main-title'>NexMove: Mobility Data at Your Fingertips</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='subtitle'>Interactive Data Analysis</h2>", unsafe_allow_html=True)

    # Divider
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Verify that the DataFrame DATA is loaded and contains the 'day' column
    if 'day' in DATA.columns:
        DATA['day'] = pd.to_datetime(DATA['day'], errors='coerce')
    else:
        st.error("Error: The 'day' column is not found in the DataFrame DATA.")
        st.stop()

    # Analysis for Origin Province
    st.write("### Select Origin Province for Mobility Analysis")
    provinces = DATA['provincia_origen_name'].unique()
    selected_province = st.selectbox("Select Province", provinces)

    st.write("### Select a Time Period for Origin Province")
    start_date_origin_province = st.date_input(
        "Start Date", value=pd.to_datetime("2022-01-01"),
        min_value=pd.to_datetime("2022-01-01"),
        max_value=pd.to_datetime("2024-12-31"),
        key="start_date_origin_province"
    )
    end_date_origin_province = st.date_input(
        "End Date", value=pd.to_datetime("2022-12-31"),
        min_value=pd.to_datetime("2022-01-01"),
        max_value=pd.to_datetime("2024-12-31"),
        key="end_date_origin_province"
    )

    filtered_data_origin_province = DATA[
        (DATA['provincia_origen_name'] == selected_province) &
        (DATA['day'] >= pd.to_datetime(start_date_origin_province)) &
        (DATA['day'] <= pd.to_datetime(end_date_origin_province))
    ]

    if not filtered_data_origin_province.empty:
        daily_travelers_origin_province = filtered_data_origin_province.groupby('day')['viajeros'].sum().reset_index()
        daily_travelers_origin_province['day'] = daily_travelers_origin_province['day'].dt.strftime('%Y-%m-%d')

        st.write(f"## Mobility Data for {selected_province} (Origin)")
        daily_travelers_origin_province.set_index('day', inplace=True)
        st.bar_chart(daily_travelers_origin_province['viajeros'])
    else:
        st.write("No data available for the selected origin province and date range.")

    # Divider
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Analysis for Destination Province
    st.write("### Select Destination Province for Mobility Analysis")
    destination_provinces = DATA['provincia_destino_name'].unique()
    selected_province_dest = st.selectbox("Select Destination Province", destination_provinces)

    st.write("### Select a Time Period for Destination Province")
    start_date_dest_province = st.date_input(
        "Start Date", value=pd.to_datetime("2022-01-01"),
        min_value=pd.to_datetime("2022-01-01"),
        max_value=pd.to_datetime("2024-12-31"),
        key="start_date_dest_province"
    )
    end_date_dest_province = st.date_input(
        "End Date", value=pd.to_datetime("2022-12-31"),
        min_value=pd.to_datetime("2022-01-01"),
        max_value=pd.to_datetime("2024-12-31"),
        key="end_date_dest_province"
    )

    filtered_data_dest_province = DATA[
        (DATA['provincia_destino_name'] == selected_province_dest) &
        (DATA['day'] >= pd.to_datetime(start_date_dest_province)) &
        (DATA['day'] <= pd.to_datetime(end_date_dest_province))
    ]

    if not filtered_data_dest_province.empty:
        daily_travelers_dest_province = filtered_data_dest_province.groupby('day')['viajeros'].sum().reset_index()
        daily_travelers_dest_province['day'] = daily_travelers_dest_province['day'].dt.strftime('%Y-%m-%d')

        st.write(f"## Mobility Data for {selected_province_dest} (Destination)")
        daily_travelers_dest_province.set_index('day', inplace=True)
        st.bar_chart(daily_travelers_dest_province['viajeros'])
    else:
        st.write("No data available for the selected destination province and date range.")

    # Divider
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Autonomous Community Analysis
    st.write("### Select Origin Autonomous Community for Mobility Analysis")
    origin_communities = DATA['comunidad_origen'].unique()
    selected_origin_community = st.selectbox("Select Origin Autonomous Community", origin_communities)



    st.write("### Select a Time Period for Destination Autonomous Community")
    start_date_origin_community = st.date_input(
        "Start Date", value=pd.to_datetime("2022-01-01"),
        min_value=pd.to_datetime("2022-01-01"),
        max_value=pd.to_datetime("2024-12-31"),
        key="start_date_origin_community"
    )
    end_date_origin_community = st.date_input(
        "End Date", value=pd.to_datetime("2022-12-31"),
        min_value=pd.to_datetime("2022-01-01"),
        max_value=pd.to_datetime("2024-12-31"),
        key="end_date_origin_community"
    )

    filtered_data_origin_community = DATA[
        (DATA['comunidad_origen'] == selected_origin_community) &
        (DATA['day'] >= pd.to_datetime(start_date_origin_community)) &
        (DATA['day'] <= pd.to_datetime(end_date_origin_community))
    ]

    if not filtered_data_origin_community.empty:
        daily_travelers_origin_community = filtered_data_origin_community.groupby('day')['viajeros'].sum().reset_index()
        daily_travelers_origin_community['day'] = daily_travelers_origin_community['day'].dt.strftime('%Y-%m-%d')

        st.write(f"## Mobility Data for {selected_origin_community} (Origin)")
        daily_travelers_origin_community.set_index('day', inplace=True)
        st.bar_chart(daily_travelers_origin_community['viajeros'])
    else:
        st.write("No data available for the selected origin autonomous community and date range.")



    # Divider
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.write("### Select Destination Autonomous Community for Mobility Analysis")
    destination_communities = DATA['comunidad_destino'].unique()
    selected_destination_community = st.selectbox("Select Destination Autonomous Community", destination_communities)

    st.write("### Select a Time Period for Destination Autonomous Community")
    start_date_destination_community = st.date_input(
        "Start Date", value=pd.to_datetime("2022-01-01"),
        min_value=pd.to_datetime("2022-01-01"),
        max_value=pd.to_datetime("2024-12-31"),
        key="start_date_destination_community"
    )
    end_date_destination_community = st.date_input(
        "End Date", value=pd.to_datetime("2022-12-31"),
        min_value=pd.to_datetime("2022-01-01"),
        max_value=pd.to_datetime("2024-12-31"),
        key="end_date_destination_community"
    )

    filtered_data_destination_community = DATA[
        (DATA['comunidad_origen'] == selected_destination_community) &
        (DATA['day'] >= pd.to_datetime(start_date_destination_community)) &
        (DATA['day'] <= pd.to_datetime(end_date_destination_community))
    ]

    if not filtered_data_destination_community.empty:
        daily_travelers_destination_community = filtered_data_destination_community.groupby('day')['viajeros'].sum().reset_index()
        daily_travelers_destination_community['day'] = daily_travelers_destination_community['day'].dt.strftime('%Y-%m-%d')

        st.write(f"## Mobility Data for {selected_destination_community} (Destination)")
        daily_travelers_destination_community.set_index('day', inplace=True)
        st.bar_chart(daily_travelers_destination_community['viajeros'])
    else:
        st.write("No data available for the selected destination autonomous community and date range.")


if __name__ == "__main__":
    main()
