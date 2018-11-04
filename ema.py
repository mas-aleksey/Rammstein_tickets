from gateway import DB


class EmaModule:
    def __init__(self, last_price):
        self.gateway = DB()
        self.init(last_price)

    def init(self, price):
        ema = self.gateway.get_ema()
        if not ema:
            self.gateway.set_ema({1: price, 200: price, 750: price, 1500: price})

    def get(self):
        return self.gateway.get_ema()

    def update(self, value):
        ema_dict = self.gateway.get_ema()
        new_ema_dict = {p: self.calc_ema(value, p, v) for p, v in ema_dict.items()}
        self.gateway.set_ema(new_ema_dict)
        return new_ema_dict

    @staticmethod
    def calc_ema(value, period, old_ema):
        a = 2 / (period + 1)
        new_ema = a * value + (1 - a) * old_ema
        return new_ema
