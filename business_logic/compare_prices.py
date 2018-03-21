from interface.interface import Interface


class ComparePrices:
    def __init__(self):
        self.itf = Interface()

    def get_prices(self):
        binance_prices = self.itf.get_prices(self.itf.MARKET_BINANCE)
        gdax_prices = self.itf.get_prices(self.itf.MARKET_GDAX)
        all_prices = {'binance': binance_prices,
                      'gdax': gdax_prices}
        keys = set(binance_prices.keys()) | set(gdax_prices.keys())  # gets distinct values
        max_market_book = {}
        for symbol in keys:
            max_bid = 0
            min_ask = 1000000000
            for exchange in all_prices.keys():

                if symbol in all_prices[exchange]:
                    symbol_prices = all_prices[exchange][symbol]
                    # bid_price = all_prices[exchange][symbol]
                    # bid_float_prices = [float(i) for i in all_prices[exchange][symbol]['bids'][0]]
                    # ask_float_prices = [float(i) for i in all_prices[exchange][symbol]['asks'][0]]
                    if symbol_prices['bidPrice'] > max_bid:
                        max_bid = symbol_prices['bidPrice']
                        quantity_bid = symbol_prices['bidQty']
                        max_exchange = exchange
                    if symbol_prices['askPrice'] < min_ask:
                        min_ask = symbol_prices['askPrice']
                        quantity_ask = symbol_prices['askQty']
                        min_exchange = exchange
            max_market_book[symbol] = {'bids': {'exchange': max_exchange,
                                                'price': max_bid,
                                                'quantity': quantity_bid},
                                       'asks': {'exchange': min_exchange,
                                                'price': min_ask,
                                                'quantity': quantity_ask}
                                       }
        return max_market_book

    def pricing_compare(self):
        prices = self.get_prices()
        # print(prices)
        profitable_symbols = {}
        for symbol in prices.keys():
            bids = prices[symbol]['bids']
            asks = prices[symbol]['asks']
            difference = bids['price'] - asks['price']
            if difference > 0:
                print('%s dollar dollar %s', (symbol, difference))
                print(prices[symbol])
                profitable_symbols[symbol] = prices[symbol]
        return profitable_symbols
