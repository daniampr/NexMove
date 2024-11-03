'''


'''
import pandas as pd


def load_csv(file_path):
    '''
    Load a CSV file into a pandas DataFrame.
    Parameters:
        file_path (str): The path to the CSV file.
    Returns:
        pd.DataFrame: The DataFrame containing the data from the CSV file.
    '''
    return pd.read_csv(file_path)