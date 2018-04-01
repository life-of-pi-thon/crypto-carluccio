from business_logic.create_order import CreateOrder
from binance.client import Client as BinanceClient
from interface.interface import Interface
import time

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

    def place_orders(self, arbs):
        interface = Interface()
        for product in arbs.keys():
            bid_ask = arbs[product]
            quantity = min(bid_ask["bids"]["quantity"], bid_ask["asks"]["quantity"])
            bids = bid_ask["bids"]
            asks = bid_ask["asks"]
            # first buy then if the order is filled and the arb is still valid then sell
            buy_response = interface.create_test_order(bids['exchange'], product, bids['side'], 'limit', quantity, price=bids['price'])
            buy_order_id = buy_response['id']
            order_filled = False
            while not order_filled:
                if interface.order_filled(bids['exchange'], buy_order_id):
                    print('bought')
                    order_filled = True
                else:
                    time.sleep(5)

            sell_response = interface.create_test_order(asks['exchange'], product, asks['side'], 'limit', quantity, price=asks['price'])
            sell_order_id = sell_response['id']
            order_filled = False
            while not order_filled:
                if interface.order_filled(asks['exchange'], sell_order_id):
                    print('sold, arbitrage complete')
                    order_filled = True
                else:
                    time.sleep(5)
