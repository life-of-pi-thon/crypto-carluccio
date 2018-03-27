from business_logic.create_order import CreateOrder
from binance.client import Client as BinanceClient
from interface.interface import Interface

class Logic:
    def __init__(self):
        self.creator = CreateOrder()

    def logic_to_create(self):
        #TODO may be worth removing the additional creator layer
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

    def place_test_orders(self, arbs):
        interface = Interface()
        for product in arbs.keys():
            bid_ask = arbs[product]
            quantity = min(bid_ask["bids"]["quantity"], bid_ask["asks"]["quantity"])
            # For now just submit a limit order buy and sell at the same time.
            for key in bid_ask:
                if key == 'bids':
                    side = 'sell'
                elif key == 'asks':
                    side = 'buy'
                data = bid_ask[key]
                interface.create_test_order(data['exchange'], product, side, 'limit', quantity, price=data['price'])
