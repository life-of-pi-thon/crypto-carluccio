from exchange_fees import binance_fees, gdax_fees


class exchangeFees:
    #fee_type
    TYPE_FIXED = 'fixed'
    TYPE_DECIMAL = 'decimal'

    #wdt_fee
    WITHDRAWAL_FEES = 'withdrawal_fees'
    DEPOSIT_FEES = 'deposit_fees'
    TRADING_FEES = 'trading_fees'

    def __init__(self, symbol, exchange):
        self.withdrawal_fee_type = None
        self.withdrawal_fee = None
        self.deposit_fee_type = None
        self.deposit_fee = None
        self.trading_fee_type = None
        self.trading_fee = None
        self.set_fees(symbol, exchange)

    def set_fees(self, symbol, exchange):
        all_exchange_fees = dict(binance_fees.fees, **gdax_fees.fees)
        specific_exchange_fees = all_exchange_fees[exchange]

        def get_fee_type_and_amount(wdt_fee): #wdt withdrawal deposit trading
            fee_type = specific_exchange_fees[wdt_fee]["type"]
            if fee_type == exchangeFees.TYPE_DECIMAL: fee =  specific_exchange_fees[wdt_fee]["value"]
            else:
                for wdt_symbol in specific_exchange_fees[wdt_fee]["value"].keys():
                    if symbol.startswith(wdt_symbol):
                        fee = specific_exchange_fees[wdt_fee]["value"][wdt_symbol]
            return (fee_type, fee)

        (self.withdrawal_fee_type, self.withdrawal_fee) = get_fee_type_and_amount(exchangeFees.WITHDRAWAL_FEES)
        (self.deposit_fee_type, self.deposit_fee) = get_fee_type_and_amount(exchangeFees.DEPOSIT_FEES)
        (self.trading_fee_type, self.trading_fee) = get_fee_type_and_amount(exchangeFees.TRADING_FEES)

    def generic_order_fee_calculator(self, fee_type, fee, quantity):
        if fee_type == exchangeFees.TYPE_FIXED:
            new_fee = fee
        else:
            new_fee = fee * quantity
        return new_fee

    def buy_order_fee(self, quantity):
        return self.generic_order_fee_calculator(self.trading_fee_type, self.trading_fee, quantity)

    def full_withdrawal_fee(self, quantity):
        return self.generic_order_fee_calculator(self.withdrawal_fee_type, self.withdrawal_fee, quantity)

    def full_deposit_fee(self, quantity):
        return self.generic_order_fee_calculator(self.deposit_fee_type, self.deposit_fee, quantity)

    def sell_order_fee(self, quantity):
        return self.generic_order_fee_calculator(self.trading_fee_type, self.trading_fee, quantity)
