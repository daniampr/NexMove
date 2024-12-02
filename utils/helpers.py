import pandas as pd
import base64
import streamlit as st


@st.cache_data
def load_dataset_main():

    # Carga los tres datasets
    data1 = pd.read_csv('files/dataset/full_dataset_extended_2022.csv')
    data2 = pd.read_csv('files/dataset/full_dataset_extended_2023.csv')
    data3 = pd.read_csv('files/dataset/full_dataset_extended_2024.csv')

    # Combina los tres datasets en uno solo
    DATA = pd.concat([data1, data2, data3], ignore_index=True)
   
    # Dictionary to map month numbers to month names
    month_map = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
        7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }

    # Replace month numbers with month names in the 'month' column
    DATA['month'] = DATA['month'].replace(month_map)

    # Define the correct month order
    month_order = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]

    day_of_week_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Convert the 'month' and 'day_of_week' column to a categorical type with the specified order
    DATA['month'] = pd.Categorical(DATA['month'], categories=month_order, ordered=True)
    DATA['day_of_week'] = pd.Categorical(DATA['day_of_week'], categories=day_of_week_order, ordered=True)

    return DATA


@st.cache_data
def load_dataset_weather():

    # Load the data into a DataFrame
    df = pd.read_csv('files/dataset/weather_observation.csv', sep=';')

    # Drop the 'cod_municipio' column
    df = df.drop(columns=['cod_municipio'])

    # Convert the 'day' column to a datetime type
    df['day'] = pd.to_datetime(df['day'])

    # Create new columns for day_of_week, day_number, month, and year
    df['day_of_week'] = df['day'].dt.day_name()  # Day of the week
    df['day_number'] = df['day'].dt.day         # Day of the month
    df['month'] = df['day'].dt.month_name()     # Full month name
    df['year'] = df['day'].dt.year              # Year


    province_mapping = {
        'Rioja, La': 'La Rioja',
        'Valencia/Valéncia': 'Valencia',
        'Castellón/Castelló': 'Castellón',
        'Balears, Illes': 'Islas Baleares',
        'Araba/Álava': 'Álava',
        'Coruña, A': 'A Coruña',
        'Palmas, Las': 'Las Palmas',
    }

    # Replace province names in 'provincia_destino_name' and 'provincia_origen_name'
    df['desc_provincia'] = df['desc_provincia'].replace(province_mapping)


    # Dictionary of provinces and their capitals
    province_capitals = {
        'Alicante': 'Alicante/Alacant', 'Almería': 'Almería', 'Badajoz': 'Badajoz', 'Barcelona': 'Barcelona',
        'Castellón': 'Castellón de la Plana/Castelló de la Plana', 'Ceuta': 'Ceuta', 'Ciudad Real': 'Ciudad Real',
        'Cuenca': 'Cuenca', 'Cáceres': 'Cáceres', 'Cádiz': 'Cádiz', 'Córdoba': 'Córdoba',
        'Girona': 'Girona', 'Granada': 'Granada', 'Guadalajara': 'Guadalajara',
        'Huelva': 'Huelva', 'Jaén': 'Jaén', 'Lleida': 'Lleida', 'Madrid': 'Madrid',
        'Murcia': 'Murcia', 'Málaga': 'Málaga', 'Ourense': 'Ourense', 'Las Palmas': 'Palmas de Gran Canaria',
        'Santa Cruz de Tenerife': 'Santa Cruz de Tenerife', 'Segovia': 'Segovia', 'Sevilla': 'Sevilla', 
        'Tarragona': 'Tarragona', 'Teruel': 'Teruel', 'Toledo': 'Toledo', 'Valencia': ';València', 
        'Valladolid': 'Valladolid', 'Zaragoza': 'Zaragoza', 'Albacete': 'Albacete', 
        'Álava': 'Vitoria-Gasteiz', 'Asturias': 'Oviedo', 'Islas Baleares': 'Palma', 
        'Bizkaia': 'Bilbao', 'Burgos': 'Burgos', 'Cantabria': 'Santander', 
        'A Coruña': 'Coruña, A', 'Gipuzkoa': 'Donostia/San Sebastián', 'Huesca': 'Huesca', 
        'León': 'León', 'Lugo': 'Lugo', 'Navarra': 'Pamplona/Iruña', 'Pontevedra': 'Pontevedra', 
        'La Rioja': 'Logroño', 'Melilla': 'Melilla', 'Palencia': 'Palencia', 
        'Salamanca': 'Salamanca', 'Soria': 'Soria', 'Zamora': 'Zamora', 'Ávila': 'Ávila'
    }

    # Get the list of all capitals
    capital_list = list(province_capitals.values())

    # Filter the dataframe to keep only rows with capitals
    df_capitals = df[df['desc_municipio'].isin(capital_list)]

    # Reset the index for cleanliness
    df_capitals.reset_index(drop=True, inplace=True)
    return df_capitals


@st.cache_data
def load_dataset_chat():

    data1_chat = pd.read_csv('files/dataset/dataset_eng_withdist_2022.csv')
    data2_chat = pd.read_csv('files/dataset/dataset_eng_withdist_2023.csv')
    data3_chat = pd.read_csv('files/dataset/dataset_eng_withdist_2024.csv')

    DATA_simple_chat = pd.concat([data1_chat, data2_chat, data3_chat], ignore_index=True)

    return DATA_simple_chat


@st.cache_data
def filter_data_by_province(data, province_keys):
    return data[data['provincia_destino_name'].isin(province_keys)].copy()



# Configuración inicial
@st.cache_data
def setup_headers():

    # CSS Styling
    st.markdown(
        f"""
        <style>
        .header-container {{
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 50vh; /* Ajustar para centrar verticalmente */
            text-align: center;
            background: rgba(0, 0, 0, 0.7);
            color: #ffffff;
        }}
        .header-title {{
            font-size: 3rem;
            font-weight: bold;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
        }}
        .header-subtitle {{
            font-size: 1.5rem;
            margin: 0;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
        }}
        .logo-container {{
            margin-top: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .logo {{
            width: 150px; /* Tamaño reducido para el logo */
        }}
        .cta-buttons {{
            display: flex;
            justify-content: center;
            gap: 25px;
            margin-top: 30px;
        }}
        .cta-button {{
            background-color: #00d2ff;
            color: #ffffff;
            padding: 15px 30px;
            border: none;
            border-radius: 50px;
            font-size: 1.2rem;
            cursor: pointer;
            text-decoration: none;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
            transition: background-color 0.3s ease, transform 0.2s;
        }}
        .cta-button:hover {{
            background-color: #008fb3;
            transform: scale(1.05);
        }}
        .footer {{
            font-family: 'Arial', sans-serif;
            font-size: 0.9rem;
            text-align: center;
            color: #ffffff;
            margin-top: 40px;
            padding: 15px;
            border-top: 2px solid #00d2ff;
            background: #1b263b;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# Function to encode image to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()
