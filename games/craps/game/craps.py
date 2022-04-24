from decimal import Decimal

from games.base import Game
from uuid import UUID

from games.craps.game.round import CrapsRound

import random


class CrapsGame(Game):

    def __init__(self, session_id: UUID) -> None:
        super().__init__(session_id)

        self.round = None
        self.waiting_room = set()
        self.bets = {player: {"pass_bet": 0, "dont_pass_bet": 0, "come_bet": 0, "dont_come_bet": 0}
                     for player in self.players}
        self.players_ready = {player: False for player in self.players}
        self.shooter = None

        print("CREATED: CrapsGame object")

    def add_players_from_waiting_room(self):
        print("CALLED: add_players_from_waiting_room() in craps.py")

        for player in self.waiting_room:
            self.players.add(player)
        self.waiting_room = set()

    def all_ready(self):
        print("CALLED: all_ready() in craps.py")

        return all(self.players_ready.values())

    def get_stage(self):
        print("CALLED: get_stage() in craps.py")

        if self.round is None:
            return 'betting1'
        else:
            return self.round.get_stage()

    def ready_up(self, player, ready_state):
        print("CALLED: ready_up() in craps.py")

        self.players_ready[player] = ready_state

    def reset(self):
        print("CALLED: reset() in craps.py")

        self.round = None
        self.add_players_from_waiting_room()

        for player in self.players:
            self.bets[player] = {"pass_bet": 0, "dont_pass_bet": 0, "come_bet": 0, "dont_come_bet": 0}
            self.players_ready[player] = False

        self.choose_next_shooter()

    def choose_next_shooter(self):
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

        print("CALLED: choose_next_shooter() in CrapsGame")
        print("The chosen shooter is ", new_shooter.username)

        self.shooter = new_shooter

    def start_round(self):
        print("CALLED: start_round() in craps.py")

        for player in self.players:
            self.players_ready[player] = False

        self.choose_next_shooter()
        self.round = CrapsRound(self.players, self.shooter)

    def remove_player(self, player):
        print("CALLED: remove_player() in craps.py")

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

    def add_player(self, player):
        print("CALLED: add_player() in craps.py")

        if self.get_stage() == 'betting1':
            if player not in self.players:
                self.players.add(player)
                self.bets[player] = {"pass_bet": 0, "dont_pass_bet": 0, "come_bet": 0, "dont_come_bet": 0}
                self.players_ready[player] = False
        else:
            self.waiting_room.add(player)

    def update_pass_bets(self, player, pass_bet, dont_pass_bet):
        pass_diff = self.bets[player]['pass_bet'] - Decimal(pass_bet)
        dont_pass_diff = self.bets[player]['dont_pass_bet'] - Decimal(dont_pass_bet)

        player.update_balance(pass_diff + dont_pass_diff)

    def update_come_bets(self, player, come_bet, dont_come_bet):
        come_diff = self.bets[player]['come_bet'] - Decimal(come_bet)
        dont_come_diff = self.bets[player]['dont_come_bet'] - Decimal(dont_come_bet)

        player.update_balance(come_diff + dont_come_diff)

    def calculate_payouts(self):
        for player in self.players:
            if self.round.pass_win:
                player.update_balance(2 * self.bets[player]['pass_bet'])

            if self.round.dont_pass_win:
                player.update_balance(2 * self.bets[player]['dont_pass_bet'])

            if self.round.come_win:
                player.update_balance(2 * self.bets[player]['come_bet'])

            if self.round.dont_come_win:
                player.update_balance(2 * self.bets[player]['dont_come_bet'])

    def dict_representation(self):
        print("CALLED: dict_representation() in craps.py")

        to_return = {'stage': self.get_stage(),
                     'players': [{'player': player.username,
                                  'bet': {key: str(value) for key, value in self.bets[player].items()},
                                  'ready': self.players_ready[player],
                                  'shooter': True if player == self.shooter else False}
                                 for player in self.players],
                     'shooter': None if self.shooter is None else self.shooter.username,
                     'round': None if self.round is None else self.round.dict_representation()
                     }

        print(to_return)
        return to_return

    def __len__(self):
        return len(self.players) + len(self.waiting_room)
