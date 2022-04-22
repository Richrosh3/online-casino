from numpy.random import randint
from games.roulette.game.bets import Bets

class Wheel:
    wheel = [str(i) for i in range(0, 37)] + ['00']

    def __init__(self):
        self.result = None
        self.stage = 'betting'

    def roll(self):
        if self.stage == 'ready':
            self.result = randint(0, 37, size=1)[0]
            self.stage = 'ending'

    def get_stage(self):
        return self.stage

    def dict_representation(self):
        return {'result': self.result, 'stage': self.get_stage()}

    def payout(self, amount: int, bet: dict) -> int:
        return Bets.payout_mult(bet)*amount if Bets.is_winner(self.result, bet) else 0
