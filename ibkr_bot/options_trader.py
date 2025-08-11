from ib_insync import *
from ibkr_bot.client import IBKRClient

class OptionsTrader:
    def __init__(self, ib_client: IBKRClient):
        self.ib = ib_client.ib

    def fetch_option_chain(self, symbol: str):
        """
        Fetches the option chain for a given underlying symbol.
        """
        try:
            # First, we need to get the contract for the underlying stock
            underlying_contract = Stock(symbol, 'SMART', 'USD')
            self.ib.qualifyContracts(underlying_contract)

            # Then, we can request the option chain
            chains = self.ib.reqSecDefOptParams(underlyingSymbol=symbol, futFopExchange='', underlyingSecType='STK', underlyingConId=underlying_contract.conId)

            # The output of reqSecDefOptParams is a list of chains, where each chain is a list of strikes and expiries
            # We can process this data to build a more user-friendly structure

            option_chain = {}
            for chain in chains:
                if chain.exchange not in option_chain:
                    option_chain[chain.exchange] = {}

                expirations = option_chain[chain.exchange].get('expirations', set())
                expirations.update(chain.expirations)
                option_chain[chain.exchange]['expirations'] = expirations

                strikes = option_chain[chain.exchange].get('strikes', set())
                strikes.update(chain.strikes)
                option_chain[chain.exchange]['strikes'] = strikes

            return option_chain

        except Exception as e:
            print(f"Error fetching option chain for {symbol}: {e}")
            return None

    def get_tick_data(self, contract: Contract):
        """
        Subscribes to tick data for a given option contract.
        """
        try:
            self.ib.reqMktData(contract)
            # The tick data will be received through the IB events
            # We need to register a callback to handle the tick data
            # For now, we will just print the ticks
            self.ib.pendingTickersEvent += self.on_pending_tickers

        except Exception as e:
            print(f"Error getting tick data for {contract.symbol}: {e}")

    def on_pending_tickers(self, tickers):
        for ticker in tickers:
            print(f"Ticker: {ticker}")

    def place_option_order(self, contract: Contract, order: Order):
        """
        Places an option order.
        """
        try:
            trade = self.ib.placeOrder(contract, order)
            print(f"Placed order: {trade}")
            return trade
        except Exception as e:
            print(f"Error placing order for {contract.symbol}: {e}")
            return None

if __name__ == '__main__':
    # This is an example of how to use the OptionsTrader.
    # It will not run in the sandbox because it requires a running TWS or IB Gateway instance.

    # Create a client and connect
    client = IBKRClient()
    client.connect()

    if client.ib.isConnected():
        # Create an options trader
        trader = OptionsTrader(client)

        # Fetch option chain for AAPL
        option_chain = trader.fetch_option_chain('AAPL')
        if option_chain:
            print("Option chain for AAPL:")
            # print(option_chain) # This can be very long
            print(f"Exchanges: {list(option_chain.keys())}")
            # Get a sample expiration and strike
            sample_exchange = list(option_chain.keys())[0]
            sample_expiration = list(option_chain[sample_exchange]['expirations'])[0]
            sample_strike = list(option_chain[sample_exchange]['strikes'])[0]

            print(f"Sample expiration: {sample_expiration}, Sample strike: {sample_strike}")

            # Create an option contract
            option_contract = Option('AAPL', sample_expiration, sample_strike, 'C', 'SMART')

            # Get tick data for the option contract
            trader.get_tick_data(option_contract)

            # Place a sample order (this will not be executed)
            # Create a limit order
            limit_order = LimitOrder('BUY', 1, 0.01)

            # Place the order
            # trader.place_option_order(option_contract, limit_order)


        # Keep the connection alive for a bit to receive some data
        client.ib.sleep(10)

        # Disconnect
        client.disconnect()
