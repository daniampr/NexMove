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

# Convert the 'month' column to a categorical type with the specified order
DATA['month'] = pd.Categorical(DATA['month'], categories=month_order, ordered=True)
