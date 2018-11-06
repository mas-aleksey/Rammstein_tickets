import requests
import logging
from gateway import DB
from ema import EmaModule
from strat_control import StrategyModule

logger = logging.getLogger('Worker')


class Worker:
    def __init__(self, bot):
        self.telega = bot
        self.pair = 'BTCUSD'
        self.gateway = DB()
        self.ema_dict = EmaModule(self.gateway, self.get_last_price(self.pair))
        #self.strategies = StrategyModule(self.gateway)

    def process(self):
        try:
            price = self.get_last_price(self.pair)
            new_ema = self.ema_dict.update(price)
            #self.strategies.process(new_ema)
        except Exception as e:
            logger.error('Worker process error: {}'.format(e))

    def return_ema_format(self):
        ema = self.ema_dict.get()
        return '\n'.join('{}: {}'.format(*p) for p in ema.items())

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
