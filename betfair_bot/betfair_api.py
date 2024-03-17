import os
import logging
from typing import Optional, Dict, Any
from betfairlightweight import APIClient
from betfairlightweight.endpoints import betting
from betfairlightweight.resources import MarketBook
from dotenv import load_dotenv

load_dotenv()

class BetfairAPI:
    """
    A class to handle Betfair API interactions.
    """
    def __init__(self):
        self.username = os.getenv("BETFAIR_USERNAME")
        self.password = os.getenv("BETFAIR_PASSWORD")
        self.app_key = os.getenv("BETFAIR_APP_KEY")
        self.cert_path = os.getenv("BETFAIR_CERT_PATH")
        self.client = None
        self.logger = logging.getLogger(__name__)

    def initialize_api_client(self) -> APIClient:
        """
        Initialize the Betfair API client.
        """
        try:
            self.client = APIClient(
                self.username,
                self.password,
                app_key=self.app_key,
                certs=self.cert_path
            )
            self.client.login()
            return self.client
        except Exception as e:
            self.logger.error(f"Error initializing Betfair API client: {str(e)}")
            raise

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