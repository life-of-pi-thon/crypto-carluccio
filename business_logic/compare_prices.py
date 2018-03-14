from interface.interface import Interface
class ComparePrices:
    def __init__(self):
        self.itf = Interface()

    def get_prices(self):
        binance_prices = self.itf.get_prices(self.itf.MARKET_BINANCE)
