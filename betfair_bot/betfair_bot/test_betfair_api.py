from datetime import datetime, timedelta
import unittest
from betfairlightweight import APIClient
from betfairlightweight.endpoints import Betting
from betfairlightweight.exceptions import APIError
from betfairlightweight.resources.accountresources import AccountFunds

class BetfairAPITestCase(unittest.TestCase):
    def setUp(self):
        self.client = APIClient(
            username='penjud',
            password='L33tHe@t2024',
            app_key='mECg2P2ohk92MLXy',
            cert_files=('/home/tim/VScode Projects/Sickpuntv2/betfair_bot/Certs/client-2048.crt', '/home/tim/VScode Projects/Sickpuntv2/betfair_bot/Certs/client-2048.key')
        )
    def test_login(self):
        try:
            self.client.login()
            self.assertTrue(self.client.session_token)
        except APIError as e:
            self.fail(f"Login failed: {e}")

    def test_get_account_funds(self):
        try:
            self.client.login()
            account_funds = self.client.account.get_account_funds()
            self.assertIsInstance(account_funds, AccountFunds)
            self.assertTrue(hasattr(account_funds, 'available_to_bet_balance'))
        except APIError as e:
            self.fail(f"Get account funds failed: {e}")

    def test_list_market_catalogue(self):
        try:
            self.client.login()
            market_filter = {
                'eventTypeIds': ['7'],  # Horse Racing
                'marketCountries': ['GB'],  # United Kingdom
                'marketTypeCodes': ['WIN'],  # Win markets
            }
            market_catalogue = self.client.betting.list_market_catalogue(
                filter=market_filter,
                max_results=5
            )
            self.assertIsInstance(market_catalogue, list)
            self.assertLessEqual(len(market_catalogue), 5)
        except APIError as e:
            self.fail(f"List market catalogue failed: {e}")

    def test_place_order(self):
        try:
            self.client.login()

            # Retrieve active market IDs
            market_filter = {
                'eventTypeIds': ['7'],  # Horse Racing
                'marketCountries': ['GB'],  # United Kingdom
                'marketTypeCodes': ['WIN'],  # Win markets
                'marketStartTime': {
                    'from': (datetime.utcnow() + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'to': (datetime.utcnow() + timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M:%SZ')
                }
            }
            market_catalogue = self.client.betting.list_market_catalogue(
                filter=market_filter,
                max_results=1,
                sort='FIRST_TO_START'
            )

            if not market_catalogue:
                self.skipTest("No active markets found for placing orders.")

            market_id = market_catalogue[0]['marketId']

            # Retrieve selection IDs for the chosen market
            market_book = self.client.betting.list_market_book(
                market_ids=[market_id],
                price_projection={'priceData': ['EX_BEST_OFFERS']}
        )

            if not market_book or not market_book[0]['runners']:
                self.skipTest("No selections found for the market.")

            selection_id = market_book[0]['runners'][0]['selectionId']

            order = {
                'selectionId': selection_id,
                'side': 'BACK',
             'orderType': 'LIMIT',
                'limitOrder': {
                 'size': 2.0,
                 'price': 3.0,
                 'persistenceType': 'LAPSE'
            }
        }
            place_order_response = self.client.betting.place_orders(
            market_id=market_id,
            instructions=[order]
        )
            self.assertIsInstance(place_order_response, Betting.PlaceOrders)
            self.assertEqual(place_order_response.status, 'SUCCESS')
    
        except APIError as e:
            self.fail(f"Place order failed: {e}")

    def tearDown(self):
        try:
            self.client.logout()
        except APIError as e:
            pass

if __name__ == '__main__':
    unittest.main()