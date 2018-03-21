from business_logic.create_order import CreateOrder
from binance.client import Client as BinanceClient


class Logic:
    def __init__(self):
        self.creator = CreateOrder()

    def logic_to_create(self):
        # add in get market for poth and create buy/sell
        exchange = 'binance'
        symbol = 'BNBBTC'
        side = BinanceClient.SIDE_BUY
        type = BinanceClient.ORDER_TYPE_LIMIT
        price = 10
        quantity = 100
        print('a')
        self.creator.create_order(exchange='binance',
                                  symbol='BNBBTC',
                                  side=BinanceClient.SIDE_BUY,
                                  type=BinanceClient.ORDER_TYPE_LIMIT,
                                  price=10,
                                  quantity=100)
