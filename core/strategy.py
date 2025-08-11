import numpy as np

class Strategy:
    def __init__(self, fast_period=5, slow_period=20):
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.prices = []
        self.fast_ma = []
        self.slow_ma = []

    def update(self, price: float):
        """
        Updates the strategy with a new price.
        """
        self.prices.append(price)

        if len(self.prices) > self.slow_period:
            self.prices.pop(0)

        if len(self.prices) >= self.fast_period:
            self.fast_ma.append(np.mean(self.prices[-self.fast_period:]))
        else:
            self.fast_ma.append(None)

        if len(self.prices) >= self.slow_period:
            self.slow_ma.append(np.mean(self.prices))
        else:
            self.slow_ma.append(None)

    def get_signal(self) -> str:
        """
        Returns the trading signal based on the moving average crossover.
        """
        if len(self.fast_ma) < 2 or len(self.slow_ma) < 2:
            return 'HOLD'

        if self.fast_ma[-2] is None or self.slow_ma[-2] is None:
            return 'HOLD'

        # Check for crossover
        if self.fast_ma[-2] < self.slow_ma[-2] and self.fast_ma[-1] > self.slow_ma[-1]:
            return 'BUY'
        elif self.fast_ma[-2] > self.slow_ma[-2] and self.fast_ma[-1] < self.slow_ma[-1]:
            return 'SELL'
        else:
            return 'HOLD'

if __name__ == '__main__':
    # Example usage of the Strategy class
    strategy = Strategy()

    # Simulate some price data
    # In a real application, this data would come from the market data feed
    prices = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 109, 108, 107, 106, 105, 104, 103, 102, 101, 100]

    for price in prices:
        strategy.update(price)
        signal = strategy.get_signal()
        print(f"Price: {price}, Signal: {signal}")
