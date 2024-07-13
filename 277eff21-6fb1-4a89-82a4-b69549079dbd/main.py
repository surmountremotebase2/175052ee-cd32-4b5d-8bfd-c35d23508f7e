from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "AAPL"  # Example ticker, can be any stock
        self.ema_length = 20  # Length of EMA
        self.data_list = [Asset(self.ticker)]  # Asset data for the ticker

    @property
    def interval(self):
        return "1day"  # Daily interval for the data

    @property
    def assets(self):
        return [self.ticker]

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        ohlcv = data["ohlcv"][self.ticker]  # Getting OHLCV data for the ticker
        current_price = ohlcv[-1]["close"]  # Current closing price of the stock
        ema = EMA(self.ticker, ohlcv, self.ema_length)  # Calculating EMA

        if len(ema) == 0:
            return TargetAllocation({})  # No allocation if EMA is not available

        last_ema = ema[-1]  # Last EMA value

        if current_price > last_ema:
            # If current price is above EMA, indicate an uptrend and allocate 100% to buy
            allocation_dict = {self.ticker: 1}
        else:
            # If current price is below EMA, indicate a downtrend and allocate 0% to hold/sell
            allocation_dict = {self.ticker: 0}

        return TargetAllocation(allocation_dict)