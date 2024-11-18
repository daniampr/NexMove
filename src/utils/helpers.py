import pandas as pd

# Carga los tres datasets
data1 = pd.read_csv('../files/dataset/full_dataset_extended_2022.csv')
data2 = pd.read_csv('../files/dataset/full_dataset_extended_2023.csv')
data3 = pd.read_csv('../files/dataset/full_dataset_extended_2024.csv')

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


data1_chat = pd.read_csv('../files/dataset/dataset_eng_withdist_2022.csv')
data2_chat = pd.read_csv('../files/dataset/dataset_eng_withdist_2023.csv')
data3_chat = pd.read_csv('../files/dataset/dataset_eng_withdist_2024.csv')

DATA_simple_chat = pd.concat([data1_chat, data2_chat, data3_chat], ignore_index=True)