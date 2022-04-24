import random

class CrapsRound:

    def __init__(self, players, shooter):
        print("CREATED: CrapsRound object")

        self.players = players
        self.round_over = False
        self.stage = 'come-out'
        self.point = None
        self.shooter = shooter

        self.pass_win = False
        self.dont_pass_win = False
        self.come_win = False
        self.dont_come_win = False

    def get_stage(self):
        print("CALLED: get_stage() in CrapsRound")
        """
        Returns:
            The current stage of the game. The order goes "betting1", "come-out", "betting2", "point". After the phases
            are complete, the round is over, and it moves on to the next player's turn.
        """
        return self.stage

    def update_game(self, action):
        print("CALLED: update_game() in CrapsRound")

        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        total = die1 + die2

        print("The roll is", total, ", (", die1, "+", die2, ")")

        if action == "come_out":
            return self.come_out(total)
        else:
            return self.point_roll(total)

    def come_out(self, roll):
        print("CALLED: come_out() in CrapsRound")
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

        return roll

    def point_roll(self, roll):
        print("CALLED: point_roll() in CrapsRound")
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

        # Otherwise, you get to roll again. No matter what, return the roll value
        return roll

    def remove_player(self, player):
        print("CALLED: remove_player() in CrapsRound")
        self.players.remove(player)

    def dict_representation(self):
        print("CALLED: dict_representation() in CrapsRound")

        return {
            'round_over': self.round_over,
            'point': self.point,
            'pass_won': self.pass_win,
            'dont_pass_won': self.dont_pass_win,
            'come_won': self.come_win,
            'dont_come_won': self.dont_come_win
        }
