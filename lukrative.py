"""Script to gather IMDB keywords from 2013's top grossing movies."""
from os import path
import sys

def main():
    """Main entry point for the script."""
    extend_class_path()
    pass

def extend_class_path():
    sys.path.append(path.abspath('..'))
    print(sys.path)

if __name__ == '__main__':
    sys.exit(main())