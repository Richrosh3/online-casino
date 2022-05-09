from numpy.random import randint

from games.roulette.game.bets import Bets


class Wheel:
    wheel = [str(i) for i in range(0, 37)] + ['00']

    def __init__(self):
        self.result = -1
        self.stage = 'betting'

    def roll(self):
        """
        Spins the wheel if the wheel is ready and finds a number in the wheel
        """
        if self.stage == 'ready':
            self.result = Wheel.wheel[randint(0, 37, size=1)[0]]
            self.stage = 'ending'

    def get_stage(self) -> str:
        """
        Getter method for wheel stage

        Returns:
            string of the stage
        """
        return self.stage

    def dict_representation(self) -> dict:
        """
        Returns a dictionary representation of the wheel

        Returns:
            A dictionary of key result and stage with the result of the wheel and the wheel stage respectively
        """
        return {'result': "{} - {}".format(self.result, Bets.color_mapper[int(self.result)]), 'stage': self.stage}

    def payout(self, amount: float, bet: dict) -> float:
        """
        Returns the payout for a bet and the amount

        Args:
            amount: bet amount
            bet: a dictionary of key type and optionally nums for bet arguments
        Returns:
            float amount of the payout
        """
        return (Bets.payout_mult(bet) + 1) * amount if Bets.is_winner(self.result, bet) else 0.0
