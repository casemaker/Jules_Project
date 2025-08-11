import unittest
from unittest.mock import patch, MagicMock
from ibkr_bot.client import IBKRClient

class TestIBKRClient(unittest.TestCase):

    @patch('ibkr_bot.client.IB')
    def test_connect_and_disconnect(self, mock_ib):
        # Create a mock instance of the IB class
        mock_ib_instance = MagicMock()
        mock_ib.return_value = mock_ib_instance

        # Create an instance of our client
        client = IBKRClient()

        # Test the connect method
        client.connect()
        mock_ib_instance.connect.assert_called_once_with('127.0.0.1', 7497, clientId=1)

        # Test the disconnect method
        client.disconnect()
        mock_ib_instance.disconnect.assert_called_once()

if __name__ == '__main__':
    unittest.main()
