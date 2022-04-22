from games.base import Game
from uuid import UUID
from games.roulette.game.wheel import Wheel

from accounts.models import CustomUser


class Roulette(Game):

    def __init__(self, session_id: UUID):
        super.__init__(session_id)

        self.bet_amount = {player: 0 for player in self.players}
        self.bet_type = {player: None for player in self.players}
        self.wheel = Wheel()

    def record_bet(self, player, amount, bet_type: dict):
        self.bet_amount[player] = amount
        self.bet_type[player] = bet_type

    def reset(self):
        self.wheel = Wheel()
        for player in self.players:
            self.bet_amount[player] = 0
            self.bet_type[player] = None

    def remove_player(self, player: CustomUser):
        if player in self.players:
            self.bet_amount.pop(player)
            self.bet_type.pop(player)
            if len(self.players) == 0:
                self.reset()

    def add_player(self, player: CustomUser):
        if player not in self.players:
            self.players.add(player)
            self.bet_amount[player] = 0
            self.bet_type[player] = None

    def all_ready(self):
        return all(self.bet_amount.values())

    def start_round(self):
        self.wheel.roll()
