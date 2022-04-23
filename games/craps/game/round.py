class CrapsRound:

    def __init__(self, players, players_ready, shooter):
        self.players = players
        self.players_ready = players_ready
        self.round_over = False
        self.stage = 'betting1'
        self.point = None
        self.shooter = shooter

    def get_stage(self):
        """
        Returns:
            The current stage of the game. The order goes "betting1", "come-out", "betting2", "point". After the phases
            are complete, the round is over, and it moves on to the next player's turn.
        """
        return self.stage

    def update_game(self, player, action):
        pass
