from binance.client import Client as BinanceClient
from binance_config import settings as BinanceSettings
from gdax_config import settings as GdaxSettings
from gdax.public_client import PublicClient as GdaxPublicClient
from gdax.authenticated_client import AuthenticatedClient as GdaxAuthenticatedClient
from python_kraken.krakenex.api import API as KrakenAPI
import time

class Interface:
    def __init__(self):
        self.binanceClient = BinanceClient(BinanceSettings.api_key,
                                    BinanceSettings.api_secret)
        self.gdax_public_client = GdaxPublicClient()
        self.gdax_authenticated_client = GdaxAuthenticatedClient(key=GdaxSettings.api_key,
                                                             b64secret=GdaxSettings.api_secret,
                                                             passphrase=GdaxSettings.api_passphrase)
        self.sandbox_gdax_authenticated_client = GdaxAuthenticatedClient(key=GdaxSettings.sandbox_key,
                                                                     b64secret=GdaxSettings.sandbox_secret,
                                                                     passphrase=GdaxSettings.sandbox_passphrase,
                                                                     api_url='https://api-public.sandbox.gdax.com')
        self.kraken_public_client = KrakenAPI()

        self.MARKET_BINANCE = 'binance'
        self.MARKET_GDAX = 'gdax'
        self.MARKET_KRAKEN = 'kraken'

    def get_prices(self, exchange):
        if exchange == self.MARKET_BINANCE:
            market_books = self.binanceClient.get_products_and_prices()
        elif exchange == self.MARKET_GDAX:
            market_books = self.gdax_public_client.get_products_with_prices()
        elif exchange == self.MARKET_KRAKEN:
            market_books = self.kraken_public_client.get_market_tickers()
        else:
            print("No exchange found with name: " + exchange)
            # TODO throw exception
        return market_books

    def create_test_order(self, exchange, symbol, side, limit_market, quantity, price=0.0):
        if exchange == self.MARKET_BINANCE:
            response = self.binanceClient.create_test_order(symbol=symbol, side=side, type=limit_market,
                                                            quantity=quantity, price=price, timeInForce="GTC")
            print("order is filled")
            # The binance test order does not actually get passed to the matching engine, so we're unable to test this.

        if exchange == self.MARKET_GDAX:
            symbol_reformatted = symbol[:3] + "-" + symbol[3:]  # TODO is this correct?
            response = self.sandbox_gdax_authenticated_client.create_order(symbol=symbol_reformatted, side=side, limit_market=limit_market,
                                                                           quantity=quantity, price=price)
            order_id = response["id"]
            order_filled = False
            while not order_filled:
                order = self.sandbox_gdax_authenticated_client.get_order(order_id)
                if order["status"] == "done":
                    print("order is filled!")
                    order_filled = True
                else:
                    print("order not yet filled")
                    time.sleep(5)

    def create_order(self, exchange, symbol, side, limit_market, quantity, price=0.0):
        if exchange == self.MARKET_BINANCE:
            order = self.binanceClient.create_order(symbol, side, quantity, price, type=limit_market)
        elif exchange == self.MARKET_GDAX:
            order = self.gdax_authenticated_client.create_order(symbol, side, limit_market, quantity, price)
        else:
            print("No exchange found with name: " + exchange)
            # TODO throw exception
        print(order)

    def order_filled(self, exchange, order_id):
        if exchange == self.MARKET_BINANCE:
            return self.binanceClient.get_order(order_id)['status'] == 'done'
        elif exchange == self.MARKET_GDAX:
            return self.gdax_authenticated_client.get_order(order_id)['status'] == 'done'
        else:
            return ''
            #TODO throw exception