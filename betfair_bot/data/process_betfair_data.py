import os
import csv

def process_betfair_data():
    data_directory = 'betfair_bot/data/betfair_data'
    processed_data = []

    for filename in os.listdir(data_directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(data_directory, filename)
            with open(file_path, 'r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    # Process and extract relevant data from each row
                    # Example: Extract market ID, selection ID, odds, etc.
                    processed_row = {
                        'market_id': row['market_id'],
                        'selection_id': row['selection_id'],
                        'odds': float(row['odds']),
                        # Add more fields as needed
                    }
                    processed_data.append(processed_row)

    # Save the processed data to a file or database
    # Example: Save to a JSON file
    import json
    with open('betfair_bot/data/processed_betfair_data.json', 'w') as file:
        json.dump(processed_data, file)

if __name__ == '__main__':
    process_betfair_data()