from django.test import TestCase
from unittest import mock
from .views import place_bet

class PlaceBetTest(TestCase):
    @mock.patch('betfair_bot.views.fetch_market_data')
    def test_place_bet(self, mock_fetch_market_data):
        # Arrange
        mock_fetch_market_data.return_value = {'data': 'some market data'}

        # Act
        response = self.client.get('/place_bet/')  # Adjust the URL as needed

        # Assert
        self.assertEqual(response.status_code, 200)
        mock_fetch_market_data.assert_called_once()
