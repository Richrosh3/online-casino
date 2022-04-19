from games.base import Game
from uuid import UUID

from games.craps.game.round import CrapsRound


class CrapsGame(Game):

    def __init__(self, session_id: UUID) -> None:
        super().__init__(session_id)

        self.round = None
        self.waiting_room = set()
        self.bets = {player: {"pass": 0, "don't pass": 0, "come": 0, "don't come": 0} for player in self.players}
        self.players_ready = {player: False for player in self.players}

    def add_players_from_waiting_room(self):
        for player in self.waiting_room:
            self.players.add(player)
        self.waiting_room = set()

    def all_ready(self):
        return all(self.players_ready.values())

    def record_bet(self, player, bet_type: str, bet_amount):
        if CrapsGame.bet_type_valid(bet_type):
            self.bets[player][bet_type] += bet_amount

    @staticmethod
    def bet_type_valid(bet_type: str):
        if bet_type == "pass" or bet_type == "don't pass" or bet_type == "come" or bet_type == "don't come":
            return True
        else:
            return False

    def get_stage(self):
        return self.round.get_stage()

    def ready_up(self, player, ready_state):
        self.players_ready[player] = ready_state

    def reset(self):
        self.round = None
        self.add_players_from_waiting_room()

        for player in self.players:
            self.bets[player] = {"pass": 0, "don't pass": 0, "come": 0, "don't come": 0}
            self.players_ready[player] = False

    def start_round(self):
        for player in self.players:
            self.players_ready[player] = False

        self.round = CrapsRound(self.players, self.players_ready)

    def remove_player(self, player):
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
        if self.get_stage() == 'betting1':
            if player not in self.players:
                self.players.add(player)
                self.bets[player] = {"pass": 0, "don't pass": 0, "come": 0, "don't come": 0}
                self.players_ready[player] = False
        else:
            self.waiting_room.add(player)

    def dict_representation(self):
        return {'stage': self.get_stage(),
                'players': [{'player': player.username,
                             'bet': str(self.bets[player]),
                             'ready': self.players_ready[player]} for player in self.players]
                }

    def __len__(self):
        return len(self.players) + len(self.waiting_room)
