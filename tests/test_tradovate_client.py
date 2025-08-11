import unittest
import json
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from tradovate_bot.client import TradovateClient

class TestTradovateClient(unittest.IsolatedAsyncioTestCase):

    @patch('websockets.connect')
    async def test_run(self, mock_connect):
        # Create a mock for the websocket connection
        mock_websocket = AsyncMock()

        # websockets.connect returns an async context manager
        mock_context_manager = AsyncMock()
        mock_context_manager.__aenter__.return_value = mock_websocket
        mock_connect.return_value = mock_context_manager

        # Create an instance of our client
        client = TradovateClient(username='testuser', password='testpassword', device_id='testdevice')

        # Mock the receive method to return a successful authentication response
        # and then some other messages
        auth_response = {"d": {"accessToken": "test_token"}}
        msg1 = {"e": "md", "d": {"quotes": [{"contractId": 1, "bid": 100}]}}
        msg2 = {"e": "md", "d": {"quotes": [{"contractId": 1, "ask": 101}]}}

        mock_websocket.recv.side_effect = [
            json.dumps(auth_response),
            json.dumps(msg1),
            json.dumps(msg2),
            asyncio.CancelledError # To stop the loop
        ]

        # Create a mock message handler
        mock_handler = AsyncMock()

        # Run the client
        with self.assertRaises(asyncio.CancelledError):
            await client.run(mock_handler)

        # Check that websockets.connect was called correctly
        mock_connect.assert_called_once_with('wss://demo.tradovateapi.com/v1/websocket')

        # Check that the authentication request was sent
        self.assertEqual(mock_websocket.send.call_count, 1)
        sent_message = json.loads(mock_websocket.send.call_args[0][0])
        self.assertEqual(sent_message['url'], 'auth/accesstokenrequest')
        self.assertEqual(sent_message['body']['name'], 'testuser')

        # Check that the access token was set
        self.assertEqual(client.access_token, 'test_token')

        # Check that the handler was called with the messages
        self.assertEqual(mock_handler.call_count, 2)
        mock_handler.assert_any_call(json.dumps(msg1))
        mock_handler.assert_any_call(json.dumps(msg2))


if __name__ == '__main__':
    unittest.main()
