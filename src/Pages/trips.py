import streamlit as st
import numpy as np
import pandas as pd
from utils.helpers import DATA

st.set_page_config(layout="wide")

st.header("NexMove: Mobility data at your fingertips", anchor=False, divider="red")
st.subheader('INTERACTIVE DATA')

# Verificar que el DataFrame DATA esté cargado y contenga la columna 'day'
if 'day' in DATA.columns:
    # Convertir la columna 'day' al formato de fecha
    DATA['day'] = pd.to_datetime(DATA['day'], errors='coerce')
else:
    st.error("Error: La columna 'day' no se encuentra en el DataFrame DATA.")
    st.stop()  # Detener ejecución si la columna 'day' no existe

# Selección de Provincia de Origen
st.write("### Select Origin Province for Mobility Analysis")
provinces = DATA['provincia_origen_name'].unique()  # Provincias de origen
selected_province = st.selectbox("Select Province", provinces)

# Inputs de fecha para seleccionar el período de tiempo, limitados entre 2022 y 2024 para provincia de origen
st.write("### Select a Time Period for Origin Province")
start_date_origin = st.date_input("Start Date", value=pd.to_datetime("2022-01-01"), 
                                  min_value=pd.to_datetime("2022-01-01"), 
                                  max_value=pd.to_datetime("2024-12-31"), 
                                  key="start_date_origin")
end_date_origin = st.date_input("End Date", value=pd.to_datetime("2022-12-31"), 
                                min_value=pd.to_datetime("2022-01-01"), 
                                max_value=pd.to_datetime("2024-12-31"), 
                                key="end_date_origin")

# Filtrar los datos en función de la provincia de origen seleccionada y el rango de fechas
filtered_data_origin = DATA[
    (DATA['provincia_origen_name'] == selected_province) &
    (DATA['day'] >= pd.to_datetime(start_date_origin)) &
    (DATA['day'] <= pd.to_datetime(end_date_origin))
]

# Verificar si hay datos en el filtro aplicado para la provincia de origen
if not filtered_data_origin.empty:
    # Agrupar por día y sumar la columna 'viajeros' para la provincia de origen y rango de fechas seleccionados
    daily_travelers_origin = filtered_data_origin.groupby('day')['viajeros'].sum().reset_index()
    daily_travelers_origin['day'] = daily_travelers_origin['day'].dt.strftime('%Y-%m-%d')  # Convertir fecha a string

    # Crear el gráfico de barras con st.bar_chart
    st.write(f"## Mobility Data for {selected_province} (Origin) from {start_date_origin} to {end_date_origin}")
    daily_travelers_origin.set_index('day', inplace=True)  # Establecer 'day' como índice para el gráfico
    st.bar_chart(daily_travelers_origin['viajeros'])  # Mostrar gráfico de barras
else:
    st.write("No data available for the selected origin province and date range.")

# Selección de Provincia de Destino
st.write("### Select Destination Province for Mobility Analysis")
destination_provinces = DATA['provincia_destino_name'].unique()  # Provincias de destino
selected_province_dest = st.selectbox("Select Destination Province", destination_provinces)

# Inputs de fecha para seleccionar el período de tiempo, limitados entre 2022 y 2024 para provincia de destino
st.write("### Select a Time Period for Destination Province")
start_date_dest = st.date_input("Start Date", value=pd.to_datetime("2022-01-01"), 
                                min_value=pd.to_datetime("2022-01-01"), 
                                max_value=pd.to_datetime("2024-12-31"), 
                                key="start_date_dest")
end_date_dest = st.date_input("End Date", value=pd.to_datetime("2022-12-31"), 
                              min_value=pd.to_datetime("2022-01-01"), 
                              max_value=pd.to_datetime("2024-12-31"), 
                              key="end_date_dest")

# Filtrar los datos en función de la provincia de destino seleccionada y el rango de fechas
filtered_data_dest = DATA[
    (DATA['provincia_destino_name'] == selected_province_dest) &
    (DATA['day'] >= pd.to_datetime(start_date_dest)) &
    (DATA['day'] <= pd.to_datetime(end_date_dest))
]

# Verificar si hay datos en el filtro aplicado para la provincia de destino
if not filtered_data_dest.empty:
    # Agrupar por día y sumar la columna 'viajeros' para la provincia de destino y rango de fechas seleccionados
    daily_travelers_dest = filtered_data_dest.groupby('day')['viajeros'].sum().reset_index()
    daily_travelers_dest['day'] = daily_travelers_dest['day'].dt.strftime('%Y-%m-%d')  # Convertir fecha a string

    # Crear el gráfico de barras con st.bar_chart
    st.write(f"## Mobility Data for {selected_province_dest} (Destination) from {start_date_dest} to {end_date_dest}")
    daily_travelers_dest.set_index('day', inplace=True)  # Establecer 'day' como índice para el gráfico
    st.bar_chart(daily_travelers_dest['viajeros'])  # Mostrar gráfico de barras
else:
    st.write("No data available for the selected destination province and date range.")
