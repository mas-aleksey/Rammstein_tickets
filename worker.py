import requests
import logging
from ema import EmaModule

logger = logging.getLogger('Worker')


class Worker:
    def __init__(self, bot):
        self.telega = bot
        self.pair = 'BTCUSD'
        self.ema_dict = EmaModule(self.get_last_price(self.pair))

    def process(self):
        price = self.get_last_price(self.pair)
        self.ema_dict.update(price)
        #self.telega.push('sec: {}, price: {}'.format(datetime.datetime.now(), price))

    @staticmethod
    def get_last_price(pair):
        try:
            url = 'https://api.bitfinex.com/v1/pubticker/{}'.format(pair)
            response = requests.request("GET", url)
            last_price = float(response.json()['last_price'])
        except Exception as e:
            logger.error("In func: get_last_price for pair %s: %s" % pair, e)
        else:
            return last_price

    def return_ema_format(self):
        ema = self.ema_dict.get()
        if ema:
            return '\n'.join('{}: {}'.format(*p) for p in ema.items())
        else:
            return 'ошибка при получении ema'
