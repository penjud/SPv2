import unittest
from betfairlightweight import APIClient
from betfairlightweight.exceptions import APIError

class BetfairAPITestCase(unittest.TestCase):
    def setUp(self):
        self.client = APIClient(
            username='penjud',
            password='L33tHe@t2024',
            app_key='mECg2P2ohk92MLXy',
            cert_files=('/home/tim/VScode Projects/Sickpuntv2/client-2048.crt', '/home/tim/VScode Projects/Sickpuntv2/client-2048.key')
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
            self.assertIsInstance(account_funds, dict)
            self.assertIn('availableToBetBalance', account_funds)
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

    def tearDown(self):
        self.client.logout()

if __name__ == '__main__':
    unittest.main()