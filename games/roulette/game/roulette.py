from games.base import Game
from uuid import UUID
from games.roulette.game.wheel import Wheel

from accounts.models import CustomUser


class Roulette(Game):

    def __init__(self, session_id: UUID):
        super.__init__(session_id)

        self.bets = {players: 0 for players in self.players}
        self.wheel = Wheel()

    def record_bet(self, player, amount):
        self.bets[player] = amount

    def reset(self):
        self.wheel = Wheel()
        for player in self.players:
            self.bets[player] = 0

    def remove_player(self, player: CustomUser):
        if player in self.players:
            self.bets.pop(player)
            if len(self.players) == 0:
                self.reset()

    def add_player(self, player: CustomUser):
        if player not in self.players:
            self.players.add(player)
            self.bets[player] = 0

    def all_ready(self):
        return all(self.bets.values())

    def start_round(self):
        self.wheel.roll()
