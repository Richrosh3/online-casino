
from games.base import Game
import random
from collections import Counter
from decimal import Decimal


class Slots(Game):
    def __init__(self, session_id):
        super().__init__(session_id)

        self.bet = 0
        self.multiplier = 1

    def record_bet(self, user):
        """
        Records the players bet to the amount they requested

        Args:
            user:

        Returns:
            None
        """
        user.update_balance(-1 * Decimal(self.bet))

    def set_multiplier(self):
        """
        Sets the multiplier by following a highly skewed distribution
        The multipliers have the following probabilities of being chosen:
            1 = .75%
            2 = .15%
            3 = .07%
            4 = .02%
            5 = .01%

        Args: None
        Returns: None
        """

        rand_gen_num = random.random()

        if 0 <= rand_gen_num < .75:
            self.multiplier = 1
        if .75 <= rand_gen_num < .9:
            self.multiplier = 2
        if .9 <= rand_gen_num < .97:
            self.multiplier = 3
        if .97 <= rand_gen_num < .99:
            self.multiplier = 4
        if .99 <= rand_gen_num <= 1:
            self.multiplier = 5

    def play_slots(self):
        """
        A round of slots is played.
            Steps:
                1) Bet is placed
                2) Multiplier is randomly selected
                3) Symbols are randomly chosen
                4) Payout is calculated and sent to player

            Payout:
                The current symbols include 0-9, $, *, X, and

                If a player gets no matching numbers, they win nothing.
                If a player gets two matching numbers, they win $250
                If a player gets three matching numbers, they win $1000

                If a player gets 1 $ on the board, they win $100
                If a player gets 2 $ on the board, they win $500,
                If a player gets 3 $ on the board, they win $5000

                If a player gets 1 * on the board, they win $50
                If a player gets 2 * on the board, they win $100
                If a player gets 3 * on the board, they win $250

                If a player gets 1 X on the board, the payout will be $0
                If a player gets 2 X on the board, they lose $250
                If a player gets 3 X on the board, they lose $1000

                Combos can be made on the board.
                Examples:
                        "1 2 1" = a pre-payout of $250
                        "3 5 $" = a pre-payout of $100
                        "$ * X" = a pre-payout of $0
                        "7 7 $" = a pre-payout of $350

                The multiplier is calculated after the payout.
                total payout = pre-payout * multiplier

        Args: None
        Returns: A dictionary containing the displayed slots and payout of the player
        """

        self.set_multiplier()

        symbols = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "$", "*", "X"]
        displayed_slots = random.sample(symbols, 3)

        pre_payout = self.bet

        if "X" in displayed_slots:
            return 0

        slots_dict = dict(Counter(displayed_slots))

        for symbol in slots_dict:
            if symbol.isdigit():
                if slots_dict[symbol] == 2:
                    pre_payout *= 5
                if slots_dict[symbol] == 3:
                    pre_payout *= 20
            if symbol == "$":
                if slots_dict[symbol] == 1:
                    pre_payout *= 2
                if slots_dict[symbol] == 2:
                    pre_payout *= 10
                if slots_dict[symbol] == 3:
                    pre_payout *= 100
            if symbol == "*":
                if slots_dict[symbol] == 2:
                    pre_payout *= 20
                if slots_dict[symbol] == 3:
                    pre_payout *= 50

        payout = pre_payout * self.multiplier
        next(iter(self.players)).update_balance(Decimal(payout))

        return {"type": "spin", "displayed_slots": displayed_slots, "payout": payout}

    def dict_representation(self):
        """
        Returns the current status of a players slots session

        Args: None
        Returns: None
        """
        return {'player': next(iter(self.players)).username,
                'bet': self.bet,
                'multiplier': self.multiplier}
