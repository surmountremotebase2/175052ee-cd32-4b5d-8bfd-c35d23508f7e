from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, MACD
from surmount.logging import log
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the asset(s) to trade
        self.tickers = ["AAPL"]

    @property
    def interval(self):
        # Data fetching interval
        return "1day"

    @property
    def assets(self):
        # Assets to be considered in the trading strategy
        return self.tickers

    def run(self, data):
        # Initial allocation dict
        allocation_dict = {i: 0 for i in self.tickers} 
        
        # Loop through each ticker to calculate indicators and decide on position
        for ticker in self.tickers:
            try:
                # Calculate RSI and MACD for the ticker
                rsi = RSI(ticker, data["ohlcv"], length=14)
                macd = MACD(ticker, data["ohlcv"], fast=12, slow=26)['MACD']

                # Entry conditions (Buy signal)
                if rsi[-1] < 30 and macd[-1] > macd[-2]:  # Oversold condition with MACD bullish crossover
                    allocation_dict[ticker] = 1  # Long position
                    log(f"Buying {ticker}")

                # Exit conditions (Sell signal)
                elif rsi[-1] > 70 and macd[-1] < macd[-2]:  # Overbought condition with MACD bearish crossover
                    allocation_dict[ticker] = 0  # No position
                    log(f"Selling {ticker}")

                # Neutral/Hold condition
                else:
                    log(f"Holding {ticker}")

            except Exception as e:
                log(f"Error processing {ticker}: {e}")

        return TargetAllocation(allocation_dict)