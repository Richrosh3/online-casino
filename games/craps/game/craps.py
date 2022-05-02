import random

from accounts.models import CustomUser
from games.base import Game
from uuid import UUID

from games.craps.game.round import CrapsRound


class CrapsGame(Game):
    """
    CrapsGame is an extension of the Game class, responsible for running games of Craps.
    """

    def __init__(self, session_id: UUID) -> None:
        super().__init__(session_id)

        self.round = None
        self.waiting_room = set()
        self.bets = {player: {"pass_bet": 0, "dont_pass_bet": 0, "come_bet": 0, "dont_come_bet": 0}
                     for player in self.players}
        self.players_ready = {player: False for player in self.players}
        self.shooter = None

    def add_players_from_waiting_room(self) -> None:
        """
        Function that adds all players in the waiting room to the current list of players.
        """

        for player in self.waiting_room:
            self.players.add(player)
        self.waiting_room = set()

    def all_ready(self) -> bool:
        """
        Function to check if all players are ready.

        :return: True if all players are ready, False if there are any players that are not ready.
        """

        return all(self.players_ready.values())

    def get_stage(self) -> str:
        """
        Function to get the current stage of the game. If a CrapsRound has not been initialized, then the game is in the
        first stage of betting. Otherwise, the stage is gotten from the CrapsRound object.

        :return:    The current stage of the game.
        """

        if self.round is None:
            return 'betting1'
        else:
            return self.round.get_stage()

    def ready_up(self, player: CustomUser, ready_state: bool) -> None:
        """
        Function to set a player's ready state to a certain value.

        :param player:      The player whose value is being changed.
        :param ready_state: Boolean value to set player's ready to.
        """

        self.players_ready[player] = ready_state

    def unready_all(self) -> None:
        """
        Function to set every player's ready value to False.
        """

        for player in self.players:
            self.players_ready[player] = False

    def reset(self) -> None:
        """
        Function that resets the stage of the game. Called after all players have readied up on the game over screen.
        The round is changed back to None, any players in the waiting room are added to the game, and the bets are
        reset.
        """

        self.round = None
        self.add_players_from_waiting_room()

        for player in self.players:
            self.bets[player] = {"pass_bet": 0, "dont_pass_bet": 0, "come_bet": 0, "dont_come_bet": 0}
            self.players_ready[player] = False

    def choose_next_shooter(self) -> None:
        """
        Function to randomly determine the next shooter. Normally in Craps, the dice are passed to the left. We're using
        a set to represent the players, so that's not really feasible here, since sets are unordered. This function will
        choose a random player, with the condition that the same player can't be the shooter twice, unless there is only
        one player.
        """
        new_shooter = random.choice(tuple(self.players))

        if len(self.players) > 1:
            while new_shooter == self.shooter:
                new_shooter = random.choice(tuple(self.players))

        self.shooter = new_shooter

    def start_round(self) -> None:
        """
        Function to officially start a round of Craps, which is done after all players have finished the first phase of
        betting. A shooter is chosen and the CrapsRound object is initialized.
        """

        self.choose_next_shooter()
        self.round = CrapsRound(self.players, self.shooter)

    def remove_player(self, player: CustomUser) -> None:
        """
        Function to remove a player from the game. If the player is currently in the game and not the waiting room, they
        must be removed from the list of players, the players_ready dictionary, the bets dictionary, and the CrapsRound
        object.

        If there are no players left in the game, the game is reset. If the player is in the waiting room, they're
        simply removed from it.

        :param player:  The player to remove.
        """

        if player in self.players:
            self.players_ready.pop(player)
            self.bets.pop(player)
            if self.round is not None:
                self.round.remove_player(player)

            self.players.remove(player)

            if len(self.players) == 0:
                self.reset()

        if player in self.waiting_room:
            self.waiting_room.remove(player)

    def add_player(self, player: CustomUser) -> None:
        """
        Function to add a player to the game. If the game is still in the initial betting phase (i.e. actual gameplay
        has not started yet), the player is added to the list of players, the bets dictionary, and the players_ready
        dictionary.

        If the game is currently in progress, the player is added to the waiting room.

        :param player:  The player to add.
        """

        if self.get_stage() == 'betting1':
            if player not in self.players:
                self.players.add(player)
                self.bets[player] = {"pass_bet": 0, "dont_pass_bet": 0, "come_bet": 0, "dont_come_bet": 0}
                self.players_ready[player] = False
        else:
            self.waiting_room.add(player)

    def update_pass_bets(self, player: CustomUser, pass_bet: float, dont_pass_bet: float) -> None:
        """
        Function to update the player's pass and don't pass bets, made during the initial betting phase. The values are
        stored in the bets dictionary, and are subtracted from the player's account balance.

        :param player:          The player whose bet is being updated.
        :param pass_bet:        The pass bet value that the player has entered.
        :param dont_pass_bet:   The don't pass bet value that the player has entered.
        """
        pass_diff = self.bets[player]['pass_bet'] - pass_bet
        dont_pass_diff = self.bets[player]['dont_pass_bet'] - dont_pass_bet

        self.bets[player]['pass_bet'] = pass_bet
        self.bets[player]['dont_pass_bet'] = dont_pass_bet

        player.update_balance(pass_diff + dont_pass_diff)

    def update_come_bets(self, player: CustomUser, come_bet: float, dont_come_bet: float) -> None:
        """
        Function to update the player's come and don't come bets, made during the second betting phase. The values are
        stored in the bets dictionary, and are subtracted from the player's account balance.

        :param player:          The player whose bet is being updated.
        :param come_bet:        The come bet value that the player has entered.
        :param dont_come_bet:   The don't come bet value that the player has entered.
        """
        come_diff = self.bets[player]['come_bet'] - come_bet
        dont_come_diff = self.bets[player]['dont_come_bet'] - dont_come_bet

        self.bets[player]['come_bet'] = come_bet
        self.bets[player]['dont_come_bet'] = dont_come_bet

        player.update_balance(come_diff + dont_come_diff)

    def calculate_payouts(self) -> None:
        """
        Function that calculates the payouts for each player and adds those values to their accounts. For craps, all
        the line bets have a simple 1:1 odds, paying back the initial value that you bet, as well as that exact same
        amount on top. In other words, double what you bet.
        """
        for player in self.players:
            if self.round.pass_win:
                player.update_balance(2 * self.bets[player]['pass_bet'])

            if self.round.dont_pass_win:
                player.update_balance(2 * self.bets[player]['dont_pass_bet'])

            if self.round.come_win:
                player.update_balance(2 * self.bets[player]['come_bet'])

            if self.round.dont_come_win:
                player.update_balance(2 * self.bets[player]['dont_come_bet'])

    def dict_representation(self) -> dict:
        """
        Function to create a dictionary representation of the state of the game. The stage, list of players (and all
        associated details -- their username, their bets, their ready state, and whether they're the shooter), the
        current shooter, and the round are included.

        :return:    A dictionary representation of the state of the game.
        """
        return {'stage': self.get_stage(),
                'players': [{'player': player.username,
                             'bet': {key: str(value) for key, value in self.bets[player].items()},
                             'ready': self.players_ready[player],
                             'shooter': True if player == self.shooter else False}
                            for player in self.players],
                'shooter': None if self.shooter is None else self.shooter.username,
                'round': None if self.round is None else self.round.dict_representation()
                }

    def __len__(self) -> int:
        """
        :return:    The number of players in the game plus the number of players in the waiting room.
        """
        return len(self.players) + len(self.waiting_room)
