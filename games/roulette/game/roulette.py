from games.base import Game
from uuid import UUID
from games.roulette.game.wheel import Wheel
from games.roulette.game.bets import Bets
from json import dumps
from accounts.models import CustomUser


class Roulette(Game):

    def __init__(self, session_id: UUID):
        super().__init__(session_id)

        self.bet_amount = {player: 0 for player in self.players}
        self.bet_type = {player: None for player in self.players}
        self.payout = {player: 0 for player in self.players}
        self.wheel = Wheel()

    def record_bet(self, player, amount, bet_type: dict) -> bool:
        if Roulette.check_bet_valid(bet_type):
            self.bet_amount[player] = amount
            self.bet_type[player] = bet_type
            if self.all_ready():
                self.wheel.stage = 'ready'
            return True
        return False

    @staticmethod
    def check_bet_valid(bet_type: dict) -> bool:
        return bet_type['type'] not in Bets.BET_CHECKER or Bets.BET_CHECKER[bet_type['type']](bet_type)

    def reset(self):
        self.wheel = Wheel()
        for player in self.players:
            self.bet_amount[player] = 0
            self.bet_type[player] = None
            self.payout[player] = 0

    def remove_player(self, player: CustomUser):
        if player in self.players:
            self.bet_amount.pop(player)
            self.bet_type.pop(player)
            self.payout.pop(player)
            if len(self.players) == 0:
                self.reset()

    def add_player(self, player: CustomUser):
        if player not in self.players:
            self.players.add(player)
            self.bet_amount[player] = 0
            self.bet_type[player] = None
            self.payout[player] = 0

    def all_ready(self):
        return all(self.bet_amount.values()) and all(self.bet_type.values())

    def start_round(self):
        if self.all_ready():
            self.wheel.stage = 'ready'
        self.wheel.roll()
        self.find_payout()

    def find_payout(self):
        for player in self.payout:
            self.payout[player] = self.wheel.payout(self.bet_amount[player], self.bet_type[player])

    def dict_representation(self):
        wheel_dict = self.wheel.dict_representation()
        return {'players': [{'player': player.username,
                             'amount': str(self.bet_amount[player]),
                             'bet': dumps(self.bet_type[player]),
                             'payout': str(self.payout[player])
                             } for player in self.players]

                } | wheel_dict
