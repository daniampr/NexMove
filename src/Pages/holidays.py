import streamlit as st
import pandas as pd
import plotly.express as px
from utils.helpers import DATA

st.set_page_config(layout="wide")

st.header("NexMove: Mobility Data During Christmas Period")
st.subheader("Analyzing Mobility Patterns from December 23 to January 7")

# Verify that the DataFrame DATA is loaded and contains the 'day' column
if 'day' in DATA.columns:
    # Convert the 'day' column to datetime format
    DATA['day'] = pd.to_datetime(DATA['day'], errors='coerce')
else:
    st.error("Error: The 'day' column is not found in the DataFrame DATA.")
    st.stop()  # Stop execution if the 'day' column does not exist

# Define Christmas periods
christmas_periods = [
    ("2022-12-23", "2023-01-07"),
    ("2023-12-23", "2024-01-07")
]

# Filter the data for Christmas periods
filtered_data = pd.DataFrame()
for start_date, end_date in christmas_periods:
    period_data = DATA[(DATA['day'] >= start_date) & (DATA['day'] <= end_date)]
    filtered_data = pd.concat([filtered_data, period_data])

# Check if there is data in the applied filter
if not filtered_data.empty:
    # Add a year-season column for differentiation
    filtered_data['season'] = filtered_data['day'].apply(lambda x: f"{x.year}-{x.year + 1}" if x.month == 12 else f"{x.year - 1}-{x.year}")
    
    # Group by season, day, and sum the 'viajeros' column
    daily_travelers_christmas = filtered_data.groupby(['season', 'day'])['viajeros'].sum().reset_index()

    # Select season for analysis
    seasons = daily_travelers_christmas['season'].unique()
    selected_season = st.selectbox("Select Christmas Season", seasons)

    # Filter data by the selected season
    season_data = daily_travelers_christmas[daily_travelers_christmas['season'] == selected_season]

    # Plot the main bar chart for the selected Christmas season using Plotly
    fig = px.bar(
        season_data,
        x='day',
        y='viajeros',
        title=f"Mobility Data for Christmas Season {selected_season}",
        labels={'day': 'Date', 'viajeros': 'Number of Travelers'}
    )
    fig.update_layout(xaxis_title="Date", yaxis_title="Number of Travelers", xaxis_tickformat="%Y-%m-%d")

    st.plotly_chart(fig, use_container_width=True)

    # Breakdown by origin autonomous communities
    st.write("### Breakdown by Origin Autonomous Communities")
    origin_data = filtered_data[filtered_data['season'] == selected_season].groupby(['comunidad_origen', 'day'])['viajeros'].sum().reset_index()

    fig_origin = px.line(
        origin_data,
        x='day',
        y='viajeros',
        color='comunidad_origen',
        title=f"Origin Autonomous Community - Christmas Season {selected_season}",
        labels={'day': 'Date', 'viajeros': 'Number of Travelers', 'comunidad_origen': 'Origin Community'}
    )
    fig_origin.update_layout(
        legend=dict(
            title="Origin Community",
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.05
        ),
        xaxis_tickformat="%Y-%m-%d"
    )
    st.plotly_chart(fig_origin, use_container_width=True)

    # Breakdown by destination autonomous communities
    st.write("### Breakdown by Destination Autonomous Communities")
    dest_data = filtered_data[filtered_data['season'] == selected_season].groupby(['comunidad_destino', 'day'])['viajeros'].sum().reset_index()

    fig_dest = px.line(
        dest_data,
        x='day',
        y='viajeros',
        color='comunidad_destino',
        title=f"Destination Autonomous Community - Christmas Season {selected_season}",
        labels={'day': 'Date', 'viajeros': 'Number of Travelers', 'comunidad_destino': 'Destination Community'}
    )
    fig_dest.update_layout(
        legend=dict(
            title="Destination Community",
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.05
        ),
        xaxis_tickformat="%Y-%m-%d"
    )
    st.plotly_chart(fig_dest, use_container_width=True)
else:
    st.write("No data available for the selected Christmas periods.")


st.subheader("Analyzing Mobility Patterns from April 2 to April 9, 2023")

# Define the Easter period for 2023
easter_start = "2023-04-02"
easter_end = "2023-04-09"

# Filter the data for the Easter 2023 period
filtered_data_easter = DATA[(DATA['day'] >= easter_start) & (DATA['day'] <= easter_end)]

# Check if there is data in the applied filter for the Easter period
if not filtered_data_easter.empty:
    # Group by day and origin community, summing 'viajeros' column
    origin_data_easter = filtered_data_easter.groupby(['comunidad_origen', 'day'])['viajeros'].sum().reset_index()

    # Plot with Plotly
    fig = px.line(
        origin_data_easter,
        x='day',
        y='viajeros',
        color='comunidad_origen',
        title="Mobility by Origin Autonomous Community - Easter 2023",
        labels={'day': 'Date', 'viajeros': 'Number of Travelers', 'comunidad_origen': 'Autonomous Community'}
    )
    
    # Customize layout to place the legend on the right
    fig.update_layout(
        legend=dict(
            title="Autonomous Community",
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.05  # Position legend outside the main chart area
        )
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("No data available for Easter 2023 period.")
