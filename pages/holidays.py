import streamlit as st
import pandas as pd
import plotly.express as px
import base64  # For encoding the background image
from utils.helpers import DATA, get_base64_image


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
def holidays_main():
    setup()

    # Title and subtitle
    st.markdown("<h1 class='main-title'>NexMove: Mobility Data During Holidays</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='subtitle'>Analyzing Mobility Patterns During Key Holiday Periods</h2>", unsafe_allow_html=True)

    # Divider
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Verify that the DataFrame DATA is loaded and contains the 'day' column
    if 'day' in DATA.columns:
        DATA['day'] = pd.to_datetime(DATA['day'], errors='coerce')
    else:
        st.error("Error: The 'day' column is not found in the DataFrame DATA.")
        st.stop()

    # Christmas Analysis
    st.header("Christmas Mobility Patterns")
    christmas_periods = [("2022-12-23", "2023-01-07"), ("2023-12-23", "2024-01-07")]

    filtered_data = pd.DataFrame()
    for start_date, end_date in christmas_periods:
        period_data = DATA[(DATA['day'] >= start_date) & (DATA['day'] <= end_date)]
        filtered_data = pd.concat([filtered_data, period_data])

    if not filtered_data.empty:
        filtered_data['season'] = filtered_data['day'].apply(
            lambda x: f"{x.year}-{x.year + 1}" if x.month == 12 else f"{x.year - 1}-{x.year}"
        )

        daily_travelers_christmas = filtered_data.groupby(['season', 'day'])['viajeros'].sum().reset_index()

        seasons = daily_travelers_christmas['season'].unique()
        selected_season = st.selectbox("Select Christmas Season", seasons)

        season_data = daily_travelers_christmas[daily_travelers_christmas['season'] == selected_season]

        fig = px.bar(
            season_data,
            x='day',
            y='viajeros',
            title=f"Mobility Data for Christmas Season {selected_season}",
            labels={'day': 'Date', 'viajeros': 'Number of Travelers'}
        )
        fig.update_layout(xaxis_tickformat="%Y-%m-%d", xaxis_title="Date", yaxis_title="Number of Travelers")
        st.plotly_chart(fig, use_container_width=True)

        # Breakdown by origin autonomous communities
        st.subheader("Breakdown by Origin Autonomous Communities")
        origin_data = filtered_data[filtered_data['season'] == selected_season].groupby(
            ['comunidad_origen', 'day'])['viajeros'].sum().reset_index()

        fig_origin = px.line(
            origin_data,
            x='day',
            y='viajeros',
            color='comunidad_origen',
            title=f"Origin Autonomous Community - Christmas Season {selected_season}",
            labels={'day': 'Date', 'viajeros': 'Number of Travelers', 'comunidad_origen': 'Origin Community'}
        )
        fig_origin.update_layout(legend_title="Origin Community", xaxis_tickformat="%Y-%m-%d")
        st.plotly_chart(fig_origin, use_container_width=True)

        # Breakdown by destination autonomous communities
        st.subheader("Breakdown by Destination Autonomous Communities")
        dest_data = filtered_data[filtered_data['season'] == selected_season].groupby(
            ['comunidad_destino', 'day'])['viajeros'].sum().reset_index()

        fig_dest = px.line(
            dest_data,
            x='day',
            y='viajeros',
            color='comunidad_destino',
            title=f"Destination Autonomous Community - Christmas Season {selected_season}",
            labels={'day': 'Date', 'viajeros': 'Number of Travelers', 'comunidad_destino': 'Destination Community'}
        )
        fig_dest.update_layout(legend_title="Destination Community", xaxis_tickformat="%Y-%m-%d")
        st.plotly_chart(fig_dest, use_container_width=True)
    else:
        st.write("No data available for the selected Christmas periods.")

    # Easter Analysis
    st.header("Easter Mobility Patterns")
    easter_start, easter_end = "2023-04-02", "2023-04-09"
    filtered_data_easter = DATA[(DATA['day'] >= easter_start) & (DATA['day'] <= easter_end)]

    if not filtered_data_easter.empty:
        filtered_data_easter['season'] = "Easter 2023"
        daily_travelers_easter = filtered_data_easter.groupby(['season', 'day'])['viajeros'].sum().reset_index()

        # Main bar chart for Easter
        fig = px.bar(
            daily_travelers_easter,
            x='day',
            y='viajeros',
            title="Mobility Data for Easter 2023",
            labels={'day': 'Date', 'viajeros': 'Number of Travelers'}
        )
        fig.update_layout(xaxis_tickformat="%Y-%m-%d", xaxis_title="Date", yaxis_title="Number of Travelers")
        st.plotly_chart(fig, use_container_width=True)

        # Breakdown by origin autonomous communities
        st.subheader("Breakdown by Origin Autonomous Communities")
        origin_data_easter = filtered_data_easter.groupby(
            ['comunidad_origen', 'day'])['viajeros'].sum().reset_index()

        fig_origin = px.line(
            origin_data_easter,
            x='day',
            y='viajeros',
            color='comunidad_origen',
            title="Origin Autonomous Community - Easter 2023",
            labels={'day': 'Date', 'viajeros': 'Number of Travelers', 'comunidad_origen': 'Origin Community'}
        )
        fig_origin.update_layout(legend_title="Origin Community", xaxis_tickformat="%Y-%m-%d")
        st.plotly_chart(fig_origin, use_container_width=True)

        # Breakdown by destination autonomous communities
        st.subheader("Breakdown by Destination Autonomous Communities")
        dest_data_easter = filtered_data_easter.groupby(
            ['comunidad_destino', 'day'])['viajeros'].sum().reset_index()

        fig_dest = px.line(
            dest_data_easter,
            x='day',
            y='viajeros',
            color='comunidad_destino',
            title="Destination Autonomous Community - Easter 2023",
            labels={'day': 'Date', 'viajeros': 'Number of Travelers', 'comunidad_destino': 'Destination Community'}
        )
        fig_dest.update_layout(legend_title="Destination Community", xaxis_tickformat="%Y-%m-%d")
        st.plotly_chart(fig_dest, use_container_width=True)
    else:
        st.write("No data available for Easter 2023 period.")


if __name__ == "__main__":
    main()
