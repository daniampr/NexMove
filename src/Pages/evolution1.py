import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from utils.helpers import DATA

st.header(
        "NexMove: Mobility data at your fingertips",
        anchor=False, divider="red")

st.subheader('INTERACTIVE DATA')

#Let's create a sidebar
#st.sidebar.header("The header of the sidebar")
#st.sidebar.write("*Hello*")

#Basics line chart, area chart and bar chart
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['a', 'b', 'c'])


pivoted_data = monthly_travelers.pivot(index='month', columns='year', values='viajeros')

# Plotting a single line chart with multiple lines (one for each year)
st.write("Number of Travelers per Month (Comparison by Year)")
st.line_chart(pivoted_data)


# Ensure 'day' column is in datetime format
DATA['day'] = pd.to_datetime(DATA['day'], errors='coerce')

# Group by year and month, then sum the 'viajeros' column
monthly_travelers = DATA.groupby(['year', 'month'])['viajeros'].sum().reset_index()

# Get unique years in the dataset
years = monthly_travelers['year'].unique()

# Plotting for each year using Streamlit's line_chart
for year in years:
    st.write(f"Number of Travelers per Month in {year}")
    year_data = monthly_travelers[monthly_travelers['year'] == year]
    # Pivot the data to have 'month' as the index and 'viajeros' as the column for st.line_chart
    year_data = year_data.set_index('month')
    st.line_chart(year_data[['viajeros']])






# Get unique province names for the selection box
provinces = DATA['provincia_origen_name'].unique()

# Add a selection box for choosing a province
selected_province = st.selectbox("Select a Province", provinces)

# Filter data by the selected province
province_data = DATA[DATA['provincia_origen_name'] == selected_province]

# Group by year and month, then sum the 'viajeros' column for the selected province
monthly_travelers = province_data.groupby(['year', 'month'])['viajeros'].sum().reset_index()

# Get unique years for the selected province
years = monthly_travelers['year'].unique()

# Plotting for each year using Streamlit's line_chart
for year in years:
    st.write(f"Number of Travelers per Month in {year} with origin {selected_province}")
    year_data = monthly_travelers[monthly_travelers['year'] == year]
    # Pivot the data to have 'month' as the index and 'viajeros' as the column for st.line_chart
    year_data = year_data.set_index('month')
    st.line_chart(year_data[['viajeros']])




# Get unique province names for the selection box
provinces = DATA['provincia_destino_name'].unique()

# Add a selection box for choosing a province
selected_province_destino = st.selectbox("Select a Province", provinces)

# Filter data by the selected province
province_data = DATA[DATA['provincia_destino_name'] == selected_province_destino]

# Group by year and month, then sum the 'viajeros' column for the selected province
monthly_travelers = province_data.groupby(['year', 'month'])['viajeros'].sum().reset_index()

# Get unique years for the selected province
years = monthly_travelers['year'].unique()

# Plotting for each year using Streamlit's line_chart
for year in years:
    st.write(f"Number of Travelers per Month in {year} with destino {selected_province_destino}")
    year_data = monthly_travelers[monthly_travelers['year'] == year]
    # Pivot the data to have 'month' as the index and 'viajeros' as the column for st.line_chart
    year_data = year_data.set_index('month')
    st.line_chart(year_data[['viajeros']])


st.write("This is line chart")
#st.line_chart(DATA)

st.write("This is the area chart")
st.area_chart(chart_data)
st.write("This is the bar chart")
st.bar_chart(chart_data)


#Let's embeed a Matplotlib in our streamlit app
import matplotlib.pyplot as plt

#Example 1
arr = np.random.normal(1, 1, size=100)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)
st.write("Example 1 of plot with Matplotlib")
st.pyplot(fig)


#Seaborn: Seaborn builds on top of a Matplotlib figure so you can display the charts in the same way
import seaborn as sns
penguins = sns.load_dataset("penguins")
st.dataframe(penguins[["species", "flipper_length_mm"]].sample(6))

# Create Figure beforehand
fig = plt.figure(figsize=(9, 7))
sns.histplot(data=penguins, x="flipper_length_mm", hue="species", multiple="stack")
plt.title("Hello Penguins!")
st.write("Example of a plot with Seaborn library")
st.pyplot(fig)


#Step 10: Show a dataframe table in your app
st.dataframe(penguins[["species", "flipper_length_mm"]].sample(6))


#Creating a map Maps
#Let's create randomly a lattitude and longitud variables
df = pd.DataFrame(
np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
columns=['lat', 'lon']) #These columns are totally necessary
st.write("Example of a plot with a map")
st.map(df)


#Let's include Plotly library

import plotly.figure_factory as ff


# Add histogram data
x1 = np.random.randn(200) - 2
x2 = np.random.randn(200)
x3 = np.random.randn(200) + 2

# Group data together
hist_data = [x1, x2, x3]

group_labels = ['Group 1', 'Group 2', 'Group 3']

# Create distplot with custom bin_size
fig = ff.create_distplot(
hist_data, group_labels, bin_size=[.1, .25, .5])

# Plot!
st.write("Example of a plot with Plotly")
st.plotly_chart(fig, use_container_width=True)
