from betfairlightweight import APIClient
from betfairlightweight.endpoints import (
    login,
    keepalive,
    logout,
    betting,
    account,
    scores,
    streaming,
    inplayservice,
    racecardresource,
)
from dotenv import load_dotenv
import os

load_dotenv()  # This is the function that loads the .env file into the environment

username = os.getenv('BETFAIR_USERNAME')
password = os.getenv('BETFAIR_PASSWORD')
app_key = os.getenv('BETFAIR_APP_KEY')
cert_files = (os.getenv('BETFAIR_CERT_FILE'), os.getenv('BETFAIR_KEY_FILE'))

# Now you can use these variables in your APIClient
from betfairlightweight import APIClient

client = APIClient(username=username, password=password, app_key=app_key)
client.login()