from binance.client import Client
from binance_config import settings as BinanceSettings
from gdax_config import settings as GdaxSettings
from gdax.public_client import PublicClient
from gdax.authenticated_client import AuthenticatedClient

class Interface:

    def __init__(self):
        a=0
        self.binanceClient = Client(BinanceSettings.api_key,
                                    BinanceSettings.api_secret)
        self.gdax_public_client = PublicClient()
        self.gdax_authenticated_client = AuthenticatedClient(GdaxSettings.api_key,
                                                             GdaxSettings.api_secret,
                                                             GdaxSettings.passphrase)
        self.MARKET_BINANCE = 'binance'
        self.MARKET_GDAX = 'gdax'

    def get_prices(self, exchange):
        if exchange == self.MARKET_BINANCE:
            market_books = self.binanceClient.get_products_and_prices()
        elif exchange == self.MARKET_GDAX:
            market_books = self.gdax_public_client.get_products_with_prices()
        else:
            print("No exchange found with name: " + exchange)
            # TODO throw exception
        return market_books

    def create_test_order(self, **params):
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
        # TODO find/implement a test order


    def create_order(self, exchange, symbol, side, limit_market, quantity, price=0.0):
        if exchange == self.MARKET_BINANCE:
            order = self.binanceClient.create_order(symbol, side, quantity, price, type=limit_market)
        elif exchange == self.MARKET_GDAX:
            order = self.gdax_authenticated_client.create_order(symbol, side, limit_market, quantity, price)
        else:
            print("No exchange found with name: " + exchange)
            # TODO throw exception
        print(order)
