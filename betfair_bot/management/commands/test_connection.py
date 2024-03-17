# betfair_bot/bot/test_connection.py

import os
from betfairlightweight import APIClient
from dotenv import load_dotenv

# Load the environment variables first
load_dotenv()

# Then set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'betfair_bot.settings')
import django
django.setup()

# Now that the Django environment is set up, import Django settings
from django.conf import settings

# Function to test the Betfair API connection
def test_betfair_connection():
    username = os.getenv('BETFAIR_USERNAME')
    password = os.getenv('BETFAIR_PASSWORD')
    app_key = os.getenv('BETFAIR_APP_KEY')
    certs_path = os.getenv('BETFAIR_CERTS_PATH', settings.CERTS_DIR)  # Fallback to Django settings

    cert_file = os.path.join(certs_path, 'client-2048.crt')
    key_file = os.path.join(certs_path, 'client-2048.key')

    client = APIClient(username=username, password=password, app_key=app_key, certs=(cert_file, key_file))

    try:
        # Attempt to login
        client.login()
        print("Successfully connected to the Betfair API.")
        # Optionally, perform additional actions to test the connection further

    except Exception as e:
        print("An error occurred while attempting to connect to the Betfair API:")
        print(e)

# This will prevent the function from running if this script is imported elsewhere
if __name__ == '__main__':
    test_betfair_connection()

