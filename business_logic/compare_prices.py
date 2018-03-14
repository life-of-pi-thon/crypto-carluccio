from interface.interface import Interface
class ComparePrices:
    def __init__(self):
        self.itf = Interface()

    def get_prices(self):
        binance_prices = self.itf.get_prices(self.itf.MARKET_BINANCE)
        gdax_prices = self.itf.get_prices(self.itf.MARKET_GDAX)
        all_prices = {'binance': binance_prices,
                'gdax' : gdax_prices}
        keys = set(binance_prices.keys()) | set(gdax_prices.keys()) #gets distinct values
        max_market_book = {}
        for symbol in keys:
            for exchange in all_prices.keys():
                max_bid = 0
                min_ask = 1000000000
                if symbol in all_prices[exchange]:
                    bid_float_prices = [float(i) for i in all_prices[exchange][symbol]['bids'][0]]
                    ask_float_prices = [float(i) for i in all_prices[exchange][symbol]['asks'][0]]
                    if bid_float_prices[0] > max_bid:
                        max_bid = bid_float_prices[0]
                        quantity_bid = bid_float_prices[1]
                        max_exchange = exchange
                    if ask_float_prices[0] < min_ask:
                        min_ask = ask_float_prices[0]
                        quantity_ask = ask_float_prices[1]
                        min_exchange = exchange
            max_market_book[symbol] = {'bids' : {'exchange' : max_exchange,
                                                 'price' : max_bid,
                                                 'quantity' : quantity_bid},
                                       'asks' : {'exchange' : min_exchange,
                                                 'price' : min_ask,
                                                 'quantity' : quantity_ask}
                                       }
        return max_market_book


    def pricing_compare(self):
        prices = self.get_prices()
        #print(prices)
        for symbol in prices.keys():
            bids = prices[symbol]['bids']
            asks = prices[symbol]['asks']
            difference = asks['price'] - bids['price']
            if difference > 0:
                print('dollar dollar %s', difference)
                print(prices[symbol])
            if asks['exchange'] != bids['exchange']:
                print(prices[symbol])


