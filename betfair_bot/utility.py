import requests
from decouple import config

BETFAIR_API_KEY = config('BETFAIR_API_KEY')

def check_betfair_api_connection():
    try:
        response = requests.get('https://identitysso.betfair.com.au/api/login', timeout=5)  # Use an actual Betfair API endpoint for testing
        return response.status_code == 200
    except requests.RequestException:
        return False;