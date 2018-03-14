from binance.client import Client
from binance_config import settings as BinanceSettings
from gdax_config import settings as GdaxSettings
from gdax.public_client import PublicClient

class Interface:

    # markets
    abc = 1

    def __init__(self):
        a=0
        self.binanceClient = Client(BinanceSettings.api_key,
                        BinanceSettings.api_secret)
        self.gdax_public_client = PublicClient()
        self.MARKET_BINANCE = 'binance'
        self.MARKET_GDAX = 'gdax'

    def get_prices(self, exchange):

        if exchange == self.MARKET_BINANCE:
            #[
            # {'askQty': '0.30000000', 'askPrice': '0.07570000', 'symbol': 'ETHBTC', 'bidQty': '0.44500000', 'bidPrice': '0.07562400'},
            # {'askQty': '81.72000000', 'askPrice': '0.01912700', 'symbol': 'LTCBTC', 'bidQty': '1.89000000', 'bidPrice': '0.01912600'}
            #]

            tickers = self.binanceClient.get_orderbook_ticker()
            #prices = self.binanceClient.get_order_book('BNBBTC')
            print(tickers)
            #prices = client.get_order_book(symbol='BNBBTC')
            #print(prices)
            market_books = {}
            for market in tickers:
                symbol = market['symbol']
                market_books[symbol] = {'bids' : [[market['bidPrice'], market['bidQty']]],
                                       'asks' : [[market['askPrice'], market['askQty']]]}
            print(market_books)

        if exchange == self.MARKET_GDAX:
            currencies = self.gdax_public_client.get_products()
            symbols = []
            market_books = {}
            for currency in currencies:
                symbol = currency['display_name'].replace('/','-')
                symbols.append(symbol)
                market_book = self.gdax_public_client.get_product_order_book(symbol)
                market_books[symbol.replace('-','')] = market_book
            print(symbols)
            print(market_books)

        return market_books

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

