import streamlit as st
import pandas as pd
import base64  # Import for encoding background image
from utils.helpers import DATA


# Setup configuration and global CSS
def setup():
    st.set_page_config(
        page_title="Specific Trip Analysis",
        page_icon="🚍",
        layout="wide",
    )

    # Function to encode image to base64
    def get_base64_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()

    # Background styling
    background_image = "wallpaper.jpg"  # Path to your image file
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
    st.markdown("<h1 class='main-title'>NexMove: Mobility Data at Your Fingertips</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='subtitle'>Interactive Data: Specific Trip Analysis</h2>", unsafe_allow_html=True)

    # Divider
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Convert 'day' column to datetime format
    DATA['day'] = pd.to_datetime(DATA['day'], errors='coerce')

    # Select the year and month
    st.write("### Select a Year and Month for Analysis")
    selected_year = st.selectbox("Year", sorted(DATA['year'].unique()), index=1)
    selected_month = st.selectbox("Month", sorted(DATA['month'].unique()))

    # Filter data for the selected month and year
    filtered_month_data = DATA[(DATA['year'] == selected_year) & (DATA['month'] == selected_month)]

    # Trip Selection: Origin and Destination Provinces
    st.write("### Select Origin and Destination Provinces for the Trip")

    # Unique provinces for origin and destination
    origin_provinces = sorted(filtered_month_data['provincia_origen_name'].unique())
    destination_provinces = sorted(filtered_month_data['provincia_destino_name'].unique())

    # User selection for origin and destination provinces
    selected_origin_province = st.selectbox("Select Origin Province", origin_provinces)
    selected_destination_province = st.selectbox("Select Destination Province", destination_provinces, index=2)

    # Filter data for the selected origin and destination provinces
    filtered_trip_data_provinces = filtered_month_data[
        (filtered_month_data['provincia_origen_name'] == selected_origin_province) &
        (filtered_month_data['provincia_destino_name'] == selected_destination_province)
    ]

    # Display the line charts for provinces side by side
    if not filtered_trip_data_provinces.empty:
        st.write(f"### Number of Travelers for Trip: {selected_origin_province} to {selected_destination_province} in {selected_month}, {selected_year}")

        col1, col2 = st.columns(2)

        with col1:
            travelers_by_day_of_week = (
                filtered_trip_data_provinces.groupby('day_of_week')['viajeros']
                .sum()
            )
            st.write("#### Travelers by Day of the Week (Provinces)")
            st.line_chart(travelers_by_day_of_week, height=300, use_container_width=True)

        with col2:
            travelers_by_day_of_month = filtered_trip_data_provinces.groupby('day_number')['viajeros'].sum().sort_index()
            st.write("#### Travelers by Day of the Month (Provinces)")
            st.line_chart(travelers_by_day_of_month, height=300, use_container_width=True)
    else:
        st.write("No data available for the selected origin, destination, and date range for Provinces.")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Communities section
    st.write("### Select Origin and Destination Communities for the Trip")

    origin_communities = sorted(filtered_month_data['comunidad_origen'].unique())
    destination_communities = sorted(filtered_month_data['comunidad_destino'].unique())

    selected_origin_community = st.selectbox("Select Origin Community", origin_communities)
    selected_destination_community = st.selectbox("Select Destination Community", destination_communities)

    filtered_trip_data_communities = filtered_month_data[
        (filtered_month_data['comunidad_origen'] == selected_origin_community) &
        (filtered_month_data['comunidad_destino'] == selected_destination_community)
    ]

    if not filtered_trip_data_communities.empty:
        st.write(f"### Number of Travelers for Trip: {selected_origin_community} to {selected_destination_community} in {selected_month}, {selected_year}")

        col1, col2 = st.columns(2)

        with col1:
            travelers_by_day_of_week_communities = (
                filtered_trip_data_communities.groupby('day_of_week')['viajeros']
                .sum()
            )
            st.write("#### Travelers by Day of the Week (Communities)")
            st.line_chart(travelers_by_day_of_week_communities, height=300, use_container_width=True)

        with col2:
            travelers_by_day_of_month_communities = filtered_trip_data_communities.groupby('day_number')['viajeros'].sum().sort_index()
            st.write("#### Travelers by Day of the Month (Communities)")
            st.line_chart(travelers_by_day_of_month_communities, height=300, use_container_width=True)
    else:
        st.write("No data available for the selected origin, destination, and date range for Communities.")


if __name__ == "__main__":
    main()
