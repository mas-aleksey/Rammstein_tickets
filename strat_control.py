from strateg import Strategy


class StrategyModule:
    def __init__(self, gateway):
        self.strategies = []
        self.gateway = gateway
        self.init()

    def init(self):
        self.strategies.append(Strategy())
        self.gateway.set_strategies(self.strategies)

    def process(self, ema_dict):
        for strategy in self.strategies:
            strategy.calc(ema_dict)
