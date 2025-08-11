import json
from tradovate_bot.client import TradovateClient

class FuturesTrader:
    def __init__(self, tradovate_client: TradovateClient):
        self.client = tradovate_client

    async def subscribe_to_tick_data(self, symbol: str):
        """
        Subscribes to tick data for a given futures symbol.
        """
        if not self.client.access_token:
            print("Cannot subscribe to tick data without a valid access token.")
            return

        request = {
            "url": "md/getquote",
            "body": {
                "symbol": symbol
            }
        }
        await self.client.send(json.dumps(request))
        print(f"Subscribed to tick data for {symbol}.")

    async def on_message(self, message):
        """
        Handles incoming messages from the WebSocket.
        """
        data = json.loads(message)
        if data.get('e') == 'md' and data.get('d', {}).get('quotes'):
            for quote in data['d']['quotes']:
                print(f"Quote for {quote.get('contractId')}: {quote}")

    async def place_futures_order(self, account_id: int, symbol: str, action: str, order_type: str, quantity: int, price: float = None):
        """
        Places a futures order.
        """
        if not self.client.access_token:
            print("Cannot place an order without a valid access token.")
            return

        order = {
            "accountId": account_id,
            "contractId": None, # We need to get the contract ID for the symbol first
            "action": action,
            "orderQty": quantity,
            "orderType": order_type,
        }

        if order_type == 'Limit' and price:
            order['price'] = price

        request = {
            "url": "order/placeorder",
            "body": order
        }

        # To place an order, we first need to find the contract details for the symbol
        # This would require another request to the API (e.g., contract/find)
        # For now, we will just print the request
        print("Placing order (request not sent yet):")
        print(json.dumps(request, indent=2))

        # await self.client.send(json.dumps(request))
        # print(f"Placed order for {symbol}.")


async def main():
    # This is an example of how to use the FuturesTrader.
    # It will not run in the sandbox because it requires valid credentials.

    # IMPORTANT: Replace with your actual credentials and device ID before running
    # DO NOT COMMIT YOUR CREDENTIALS TO A PUBLIC REPOSITORY
    username = "your_username"
    password = "your_password"
    device_id = "your_unique_device_id"

    client = TradovateClient(username=username, password=password, device_id=device_id)
    # await client.connect()

    # if client.access_token:
    #     trader = FuturesTrader(client)

    #     # Subscribe to tick data for ESZ2 (E-mini S&P 500, Dec 2022)
    #     await trader.subscribe_to_tick_data('ESZ2')

    #     # Start listening for messages
    #     while True:
    #         message = await client.receive()
    #         await trader.on_message(message)

    #     # This part of the code will not be reached in this example
    #     # as the while loop above is infinite.
    #     # You would need to implement a proper exit condition.

    #     # Place a sample order (this will not be executed)
    #     # await trader.place_futures_order(123456, 'ESZ2', 'Buy', 'Limit', 1, 4000.00)

    #     await client.close()


if __name__ == '__main__':
    # To run this example, you would need to uncomment the code in main()
    # and provide your credentials.
    # asyncio.run(main())
    pass
