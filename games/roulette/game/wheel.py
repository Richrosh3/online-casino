import random
from games.roulette.game.bets import Bets

class Wheel:
    wheel = [str(i) for i in range(0, 37)] + ['00']
    color_mapper = {i: 'b' if i % 2 == 0 else 'r' for i in range(1, 11)} | \
                   {i: 'b' if i % 2 == 0 else 'r' for i in range(19, 29)} | \
                   {i: 'r' if i % 2 == 0 else 'b' for i in range(11, 19)} | \
                   {i: 'r' if i % 2 == 0 else 'b' for i in range(29, 37)}
    row_heads = [str(i) for i in range(1, 37, 3)]

    def __init__(self):
        self.result = None
        self.stage = 'betting'

    def roll(self):
        if self.stage == 'ready':
            result = round(random.uniform(0, 37)) - 1
            if result < 0:
                self.result = '00'
            else:
                self.result = str(result)
            self.stage = 'ending'

    def get_stage(self):
        return self.stage

    def dict_representation(self):
        return {'result': self.result, 'stage': self.get_stage()}

    def payout(self, amount: int, bet: dict) -> int:
        return Bets.payout_mult(bet)*amount if Bets.is_winner(self.result, bet) else 0
