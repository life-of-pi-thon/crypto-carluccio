from binance.client import Client
from config import settings as binanceSettings
client = Client(binanceSettings.api_key,
                binanceSettings.api_secret)

class interface:
    # markets
    abc = 1

    def __init__(self):
        a=0
        self.MARKET_BINANCE = 'binance'
        self.MARKET_GDAX = 'gdax'

    def get_prices(self, exchange):

        if exchange == self.MARKET_BINANCE:
            #[
            # {'askQty': '0.30000000', 'askPrice': '0.07570000', 'symbol': 'ETHBTC', 'bidQty': '0.44500000', 'bidPrice': '0.07562400'},
            # {'askQty': '81.72000000', 'askPrice': '0.01912700', 'symbol': 'LTCBTC', 'bidQty': '1.89000000', 'bidPrice': '0.01912600'}
            #]

            tickers = client.get_orderbook_ticker()
            print(tickers)
            #prices = client.get_order_book(symbol='BNBBTC')
            #print(prices)
        if exchange == SELF.MARKET_GDAX:
            tickers = []
        return tickers


