"""Script to gather IMDB keywords from 2013's top grossing movies."""
import sys
from os import path
import time
from business_logic.compare_prices import ComparePrices
import logging
logger = logging.getLogger('ftpuploader')
hdlr = logging.FileHandler('ftplog.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

def main():
    comp = ComparePrices()
    keep_alive = True

    while keep_alive:
        try:
            arbs = comp.pricing_compare()
            time.sleep(10)
            if arbs:
                logger.info(arbs)
        except Exception as e:
            keep_alive = False
            logger.error(str(e))

    """Main entry point for the script."""
    pass


def extend_class_path():
    sys.path.append(path.abspath('..'))
    print(sys.path)


if __name__ == '__main__':
    sys.exit(main())
