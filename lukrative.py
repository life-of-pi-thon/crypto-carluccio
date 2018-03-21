"""Script to gather IMDB keywords from 2013's top grossing movies."""
import sys
from os import path

from business_logic.compare_prices import ComparePrices
from business_logic.logic import Logic


def main():
    comp = ComparePrices()
    comp.pricing_compare()
    """Main entry point for the script."""
    pass


def extend_class_path():
    sys.path.append(path.abspath('..'))
    print(sys.path)


if __name__ == '__main__':
    sys.exit(main())
