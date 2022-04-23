from games.base import Game
from uuid import UUID

from games.craps.game.round import CrapsRound

import logging


class CrapsGame(Game):

    def __init__(self, session_id: UUID) -> None:
        super().__init__(session_id)

        self.round = None
        self.waiting_room = set()
        self.bets = {player: {"pass_bet": 0, "dont_pass_bet": 0, "come_bet": 0, "dont_come_bet": 0} for player in self.players}
        self.players_ready = {player: False for player in self.players}
        self.shooter = 0

        # logging.basicConfig(level=logging.DEBUG)
        logging.debug("CREATED: CrapsGame object")

    def add_players_from_waiting_room(self):
        logging.debug("CALLED: add_players_from_waiting_room() in craps.py")
        for player in self.waiting_room:
            self.players.add(player)
        self.waiting_room = set()

    def all_ready(self):
        logging.debug("CALLED: all_ready() in craps.py")
        return all(self.players_ready.values())

    def get_stage(self):
        logging.debug("CALLED: get_stage() in craps.py")
        if self.round is None:
            return 'betting1'
        else:
            return self.round.get_stage()

    def ready_up(self, player, ready_state):
        logging.debug("CALLED: ready_up() in craps.py")
        self.players_ready[player] = ready_state

    def reset(self):
        logging.debug("CALLED: reset() in craps.py")
        self.round = None
        self.add_players_from_waiting_room()

        for player in self.players:
            self.bets[player] = {"pass": 0, "don't pass": 0, "come": 0, "don't come": 0}
            self.players_ready[player] = False

        # Basically cycle through each player as the shooter until we get back to the first person again
        self.shooter += 1
        if self.shooter >= len(self.players):
            self.shooter = 0

    def start_round(self):
        logging.debug("CALLED: start_round() in craps.py")
        for player in self.players:
            self.players_ready[player] = False

        self.round = CrapsRound(self.players, self.players_ready, self.shooter)

    def remove_player(self, player):
        logging.debug("CALLED: remove_player() in craps.py")
        if player in self.players:
            self.players_ready.pop(player)
            self.bets.pop(player)
            if self.round is not None:
                self.round.remove_player(player)

            if len(self.players) == 0:
                self.reset()

        if player in self.waiting_room:
            self.waiting_room.remove(player)

    def add_player(self, player):
        logging.debug("CALLED: add_player() in craps.py")
        if self.get_stage() == 'betting1':
            if player not in self.players:
                self.players.add(player)
                self.bets[player] = {"pass_bet": 0, "dont_pass_bet": 0, "come_bet": 0, "dont_come_bet": 0}
                self.players_ready[player] = False
        else:
            self.waiting_room.add(player)

    def dict_representation(self):
        logging.debug("CALLED: dict_representation() in craps.py")
        return {'stage': self.get_stage(),
                'players': [{'player': player.username,
                             'bet': {key: str(value) for key, value in self.bets[player].items()},
                             'ready': self.players_ready[player]} for player in self.players],
                'shooter': self.shooter
                }

    def __len__(self):
        return len(self.players) + len(self.waiting_room)
