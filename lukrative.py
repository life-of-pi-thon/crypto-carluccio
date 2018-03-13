"""Script to gather IMDB keywords from 2013's top grossing movies."""
from os import path
import sys
from compare_prices import comparePrices

def main():
    comp = comparePrices()
    comp.get_prices()
    """Main entry point for the script."""
    pass

def extend_class_path():
    sys.path.append(path.abspath('..'))
    print(sys.path)

if __name__ == '__main__':
    sys.exit(main())