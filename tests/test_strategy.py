import unittest
from core.strategy import Strategy

class TestStrategy(unittest.TestCase):

    def test_moving_average_crossover(self):
        strategy = Strategy(fast_period=3, slow_period=5)

        # Downtrend
        prices = [20, 19, 18, 17, 16]
        for price in prices:
            strategy.update(price)

        self.assertEqual(strategy.get_signal(), 'HOLD')

        # Uptrend starts, but no crossover yet
        strategy.update(17)
        self.assertEqual(strategy.get_signal(), 'HOLD')

        strategy.update(18)
        self.assertEqual(strategy.get_signal(), 'HOLD')

        # Crossover happens here
        strategy.update(19)
        self.assertEqual(strategy.get_signal(), 'BUY')

        # Now, let's test a sell signal
        strategy.update(15)
        self.assertEqual(strategy.get_signal(), 'HOLD')

        strategy.update(14)
        self.assertEqual(strategy.get_signal(), 'SELL')

        strategy.update(13)
        self.assertEqual(strategy.get_signal(), 'HOLD')


if __name__ == '__main__':
    unittest.main()
