import os
import logging
from betfairlightweight import APIClient
from betfairlightweight.endpoints import betting
from betfairlightweight.resources import MarketBook
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

load_dotenv()

class BetfairAPI:
    """
    A class to handle Betfair API interactions.
    """
def get_races(self, country='AU'):
    if self.client is None:
        self.logger.error("Betfair API client is not initialized.")
        return []

    try:
        market_filter = {
            "eventTypeIds": ["7"],  # Horse Racing
            "marketCountries": [country],  # Specify the country
            "marketStartTime": {
                "from": (datetime.utcnow() + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "to": (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
            }
        }

        market_catalogue = self.client.betting.list_market_catalogue(
            filter=market_filter,
            market_projection=["MARKET_START_TIME", "EVENT", "EVENT_TYPE", "COMPETITION"],  # Add COMPETITION to the projection
            max_results=100
        )

        races = []
        for market in market_catalogue:
            race = {
                "id": market.market_id,
                "name": market.event.name,
                "venue": market.event.venue,
                "start_time": market.market_start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "competition": market.competition.name  # Add competition name to the race dictionary
            }
            races.append(race)

        return races

    except Exception as e:
        self.logger.error(f"Error retrieving races: {str(e)}")
        return []# Returning an empty list as a placeholder
def __init__(self):
    self.username = os.getenv("BETFAIR_USERNAME")
    self.password = os.getenv("BETFAIR_PASSWORD")
    self.app_key = os.getenv("BETFAIR_APP_KEY")
    self.cert_path = os.getenv("BETFAIR_CERTS_PATH")
    self.client = None
    self.logger = logging.getLogger(__name__)
    self.initialize_api_client()

    # Initialize the API client immediately if needed, or do it on demand
    self.initialize_api_client()

def initialize_api_client(self) -> None:
    try:
        self.client = APIClient(
            self.username,
            self.password,
            app_key=self.app_key,
            cert_files=(self.cert_path,)
        )
        self.client.login()
    except Exception as e:
        self.logger.error(f"Error initializing Betfair API client: {str(e)}")
        self.client = None# Consider how to handle this in your application's context

    def retrieve_races_error(self, e):
        self.logger.error(f"Error retrieving races: {str(e)}")
        pass

    def get_market_data(self, market_id: str) -> Optional[MarketBook]:
        """
        Retrieve market data for a given market ID.
        """
        try:
            market_book = self.client.betting.list_market_book(
                market_ids=[market_id],
                price_projection={"priceData": ["EX_BEST_OFFERS"]},
                order_projection="ALL",
                match_projection="ROLLED_UP_BY_PRICE"
            )

            if market_book:
                return market_book[0]
            else:
                return None
        except Exception as e:
            self.logger.error(f"Error retrieving market data: {str(e)}")
            return None

    def place_bet(self, market_id: str, selection_id: int, stake: float, odds: float, side: str = "BACK") -> None:
        """
        Place a bet on a specific market and selection.
        """
        try:
            price = self.client.betting.price_size_to_price(odds)
            instruction = {
                "selectionId": selection_id,
                "side": side,
                "orderType": "LIMIT",
                "limitOrder": {
                    "size": stake,
                    "price": price
                }
            }
            order = self.client.betting.place_orders(
                market_id=market_id,
                instructions=[instruction]
            )
            if order:
                self.logger.info(f"Bet placed successfully. Order ID: {order[0]['instructionReports'][0]['betId']}")
            else:
                self.logger.warning("Failed to place bet.")
        except Exception as e:
            self.logger.error(f"Error placing bet: {str(e)}")

    def close_connection(self) -> None:
        """
        Close the Betfair API client connection.
        """
        try:
            if self.client:
                self.client.logout()
        except Exception as e:
            self.logger.error(f"Error closing Betfair API client connection: {str(e)}")