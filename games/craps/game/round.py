import random


class CrapsRound:
    """
    CrapsRound is responsible for handling the data about an individual round of Craps. In particular, it keeps track of
    whether the game is over, the current stage, the point value, and which bet lines have won.
    """

    def __init__(self, players: set, shooter) -> None:
        self.players = players
        self.round_over = False
        self.stage = 'come-out'
        self.point = None
        self.shooter = shooter

        self.pass_win = False
        self.dont_pass_win = False
        self.come_win = False
        self.dont_come_win = False

    def get_stage(self) -> str:
        """
        Function to get the current stage of the game. The order goes "betting1", "come-out", "betting2", "point", and
        "game-over". By the time a CrapsRound object is created, the stage will be "come-out".

        :return:    The current stage of the game.
        """
        return self.stage

    def roll_dice(self, action: str) -> int:
        """
        roll_dice() is responsible for the processing of dice rolls. The dies are rolled, and the output is passed to
        the appropriate function to process the results.

        :param action:  "come_out" if the dice are being rolled during the come out phase, "point" if the dice are being
                        rolled during the point phase.

        :return:        The total number rolled.
        """
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        total = die1 + die2

        if action == "come_out":
            self.come_out(total)
        else:
            self.point_roll(total)

        return total

    def come_out(self, roll: int) -> None:
        """
        Function for the game logic of the come out roll.

        If the roll is a 2 or 3, the player has "crapped out", which means the pass line loses and the don't pass line
        wins.

        If the roll is a 12, neither pass nor don't pass win.

        If the roll is a 7 or 11, the player has rolled a "natural", which mean the pass line wins and the don't pass
        line loses.

        On any other roll, the point value is established, and we move on to the next phase of betting.

        :param roll:    The player's roll.
        """
        if roll == 2 or roll == 3:
            # Crap out, pass line loses, don't pass line wins
            self.round_over = True
            self.stage = 'game-over'
            self.dont_pass_win = True
        elif roll == 12:
            # Crap out, but it's a tie
            self.round_over = True
            self.stage = 'game-over'
        elif roll == 7 or roll == 11:
            # Natural, pass line wins, don't pass line loses
            self.round_over = True
            self.stage = 'game-over'
            self.pass_win = True
        else:
            # The point is established, and we move on to the next betting phase
            self.point = roll
            self.stage = 'betting2'

    def point_roll(self, roll: int) -> None:
        """
        Function for the game logic of the point roll.

        If the player rolls the same as the point value (as established during by come out roll), then the pass and
        come lines win. The don't pass and don't come lines lose.

        If the player rolls a 7, the don't pass and don't come lines win, while the pass and come lines lose.

        The player must continue rolling until one of those two values are rolled.

        :param roll:    The player's roll.
        """
        if roll == self.point:
            # Roll the point, pass and come win
            self.round_over = True
            self.stage = 'game-over'
            self.pass_win = True
            self.come_win = True
        elif roll == 7:
            # Roll a seven, don't pass and don't come win
            self.round_over = True
            self.stage = 'game-over'
            self.dont_pass_win = True
            self.dont_come_win = True
        else:
            # Otherwise, just keep going. Make sure the stage stays the same
            self.stage = 'point'

    def dict_representation(self) -> dict:
        """
        Function to create a dictionary representation of the state of the round. The stage, current point value, as
        well as booleans representing whether the game is over and which betting lines won, are included.

        :return:    A dictionary representation of the state of the game.
        """
        return {
            'round_over': self.round_over,
            'point': self.point,
            'pass_won': self.pass_win,
            'dont_pass_won': self.dont_pass_win,
            'come_won': self.come_win,
            'dont_come_won': self.dont_come_win
        }
