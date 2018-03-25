"""Script to gather IMDB keywords from 2013's top grossing movies."""
import sys
from os import path
import time
from business_logic.compare_prices import ComparePrices
import logging
from interface.interface import Interface
logger = logging.getLogger('ftpuploader')
hdlr = logging.FileHandler('ftplog.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

def main():
    interface = Interface()

    def place_test_orders(arbs):
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
    comp = ComparePrices()
    keep_alive = True

    while keep_alive:
        try:
            arbs = comp.pricing_compare()
            time.sleep(10)
            if arbs:
                logger.info(arbs)
                place_test_orders(arbs)
        except Exception as e:
            keep_alive = False
            logger.error(str(e))

    print(arbs)
    """Main entry point for the script."""
    pass

def extend_class_path():
    sys.path.append(path.abspath('..'))
    print(sys.path)


if __name__ == '__main__':
    sys.exit(main())
