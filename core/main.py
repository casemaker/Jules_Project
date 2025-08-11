import asyncio
from ibkr_bot.client import IBKRClient
from ibkr_bot.options_trader import OptionsTrader
from tradovate_bot.client import TradovateClient
from tradovate_bot.futures_trader import FuturesTrader
from core.strategy import Strategy

class TradingBot:
    def __init__(self):
        # Initialize the clients
        self.ibkr_client = IBKRClient()
        self.tradovate_client = TradovateClient(username='your_username', password='your_password', device_id='your_device_id')

        # Initialize the traders
        self.options_trader = OptionsTrader(self.ibkr_client)
        self.futures_trader = FuturesTrader(self.tradovate_client)

        # Initialize the strategy
        self.strategy = Strategy()

    async def run_ibkr_bot(self):
        """
        Runs the IBKR bot.
        """
        self.ibkr_client.connect()
        if self.ibkr_client.ib.isConnected():
            # Example: Fetch option chain for AAPL
            option_chain = self.options_trader.fetch_option_chain('AAPL')
            if option_chain:
                sample_exchange = list(option_chain.keys())[0]
                sample_expiration = list(option_chain[sample_exchange]['expirations'])[0]
                sample_strike = list(option_chain[sample_exchange]['strikes'])[0]

                option_contract = Contract('AAPL', sample_expiration, sample_strike, 'C', 'SMART')
                self.options_trader.get_tick_data(option_contract)

                # In a real application, we would have a loop here to process ticks
                # and generate trading signals.
                # For this example, we'll just sleep for a bit.
                await asyncio.sleep(10)

            self.ibkr_client.disconnect()

    async def run_tradovate_bot(self):
        """
        Runs the Tradovate bot.
        """
        await self.tradovate_client.connect()
        if self.tradovate_client.access_token:
            # Example: Subscribe to tick data for ESZ2
            await self.futures_trader.subscribe_to_tick_data('ESZ2')

            # In a real application, we would have a loop here to process ticks
            # and generate trading signals.
            # For this example, we'll just sleep for a bit.
            while True:
                message = await self.tradovate_client.receive()
                await self.futures_trader.on_message(message)


    async def run(self):
        """
        Runs both bots concurrently.
        """
        # In a real application, you would run these concurrently.
        # However, since we can't connect to the brokers in the sandbox,
        # we will just show the structure.

        print("Starting the trading bot...")
        # To run concurrently:
        # await asyncio.gather(
        #     self.run_ibkr_bot(),
        #     self.run_tradovate_bot()
        # )
        print("Trading bot finished.")


if __name__ == '__main__':
    bot = TradingBot()
    # Since we cannot connect to the brokers in the sandbox,
    # we will not run the bot's main loop.
    # asyncio.run(bot.run())
    print("TradingBot class is defined and ready to be used.")
    print("To run the bot, you would need to provide valid credentials and uncomment the asyncio.run(bot.run()) line.")
