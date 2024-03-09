# betfair_bot/bot/test_connection.py

from betfairlightweight import APIClient
from dotenv import load_dotenv
import os

# Load the environment variables
load_dotenv()

# Function to test the Betfair API connection
def test_betfair_connection():
    username = os.getenv('BETFAIR_USERNAME')
    password = os.getenv('BETFAIR_PASSWORD')
    app_key = os.getenv('BETFAIR_APP_KEY')
    cert_files = (os.getenv('BETFAIR_CERT_FILE'), os.getenv('BETFAIR_KEY_FILE'))

    client = APIClient(username=username, password=password, app_key=app_key, certs=cert_files)
    
    try:
        # Attempt to login
        client.login()
        print("Successfully connected to the Betfair API.")
        
        # Optionally, perform additional actions to test the connection further
        
    except Exception as e:
        print("An error occurred while attempting to connect to the Betfair API:")
        print(e)

if __name__ == '__main__':
    test_betfair_connection()
