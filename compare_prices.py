from interface import interface
class comparePrices:
    def __init__(self):
        self.itf = interface()

    def get_prices(self):
        binance_prices = self.itf.get_prices(self.itf.MARKET_BINANCE)
