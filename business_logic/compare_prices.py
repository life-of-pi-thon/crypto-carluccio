from interface.interface import Interface
from business_logic import fees

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
            if self.incorporate_fees(symbol, prices[symbol]):
                profitable_symbols[symbol] = prices[symbol]
        return profitable_symbols

    def incorporate_fees(self, symbol, order):
        #retrieve out asks/buy and bids/sell
        asks = order['asks']
        bids = order['bids']
        buy_price = asks['price']
        sell_price = bids['price']
        if sell_price - buy_price <= 0:
            return False
        else:
            quantity = min(asks['quantity'], bids['quantity'])
            original_coin_cost = quantity * buy_price

            #use class of exchange fee to get result
            asks_exchange_fees = fees.exchangeFees(symbol, asks['exchange'])
            bids_exchange_fees = fees.exchangeFees(symbol, bids['exchange'])

            #buy
            buy_order_fee = asks_exchange_fees.buy_order_fee(quantity)
            coin_post_buy = quantity - buy_order_fee

            #withdrawal
            withdrawal_fee = asks_exchange_fees.full_withdrawal_fee(coin_post_buy)
            coin_post_withdraw = coin_post_buy - withdrawal_fee

            #deposit
            deposit_fee = bids_exchange_fees.full_deposit_fee(coin_post_withdraw)
            coin_post_deposit = coin_post_withdraw - deposit_fee

            #sell
            sell_order_fee = bids_exchange_fees.sell_order_fee(coin_post_deposit)
            orignal_coin_post_sell = (coin_post_deposit - sell_order_fee) *  sell_price

            profit_loss = orignal_coin_post_sell - original_coin_cost
            #keep this for debug purposes
            if profit_loss > 0:
                print("Profit of %i, wow we're going to be rich from buying %s on %s" % (profit_loss, symbol, order))
                return True
            else:
                print("Loss of %s, wow no money from this order, better have another go here's some info %s on %s" % (profit_loss, symbol, order))
                return False
