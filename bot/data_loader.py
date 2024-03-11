import os
import json
import numpy as np
import pandas as pd

class DataLoader:
    def __init__(self, data_directory='data'):
        self.data_directory = data_directory
    
    def load_betfair_data(self, file_name='processed_betfair_data.json'):
        file_path = os.path.join(self.data_directory, file_name)
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    
    def preprocess_data(self, data):
        # Convert data to a pandas DataFrame
        df = pd.DataFrame(data)
        
        # Perform data preprocessing steps
        # Example: Convert 'odds' to decimal odds
        df['decimal_odds'] = df['odds'] + 1
        
        # Example: Calculate implied probability
        df['implied_probability'] = 1 / df['decimal_odds']
        
        # Add more preprocessing steps as needed
        
        return df