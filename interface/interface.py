from binance.client import Client
from config import settings as BinanceSettings

class Interface:
    # markets
    abc = 1

    def __init__(self):
        a=0
        self.binanceClient = Client(BinanceSettings.api_key,
                        BinanceSettings.api_secret)
        self.MARKET_BINANCE = 'binance'
        self.MARKET_GDAX = 'gdax'

    def get_prices(self, exchange):

        if exchange == self.MARKET_BINANCE:
            #[
            # {'askQty': '0.30000000', 'askPrice': '0.07570000', 'symbol': 'ETHBTC', 'bidQty': '0.44500000', 'bidPrice': '0.07562400'},
            # {'askQty': '81.72000000', 'askPrice': '0.01912700', 'symbol': 'LTCBTC', 'bidQty': '1.89000000', 'bidPrice': '0.01912600'}
            #]

            tickers = self.binanceClient.get_orderbook_ticker()
            print(tickers)
            #prices = client.get_order_book(symbol='BNBBTC')
            #print(prices)
        if exchange == self.MARKET_GDAX:
            tickers = []
        return tickers

    def create_order(self, **params):
        print(params)
        data = params['data']
        print(data)
        if data['exchange'] == self.MARKET_BINANCE:
            order = self.binanceClient.create_test_order(
                symbol=data['symbol'],
                side=data['side'],
                type=data['type'],
                quantity=data['quantity'])
            print(order)

