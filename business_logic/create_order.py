from interface.interface import Interface
class CreateOrder:
    def __init__(self):
        self.itf = Interface()

    def create_order(self, **params):
        # (self,exchange, symbol, side, type, price, quantity):
        self.itf.create_order(data=params)
