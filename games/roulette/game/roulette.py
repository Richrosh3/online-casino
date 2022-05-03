from json import dumps
from uuid import UUID

from accounts.models import CustomUser
from games.base import Game
from games.roulette.game.bets import Bets
from games.roulette.game.wheel import Wheel


class Roulette(Game):

    def __init__(self, session_id: UUID):
        super().__init__(session_id)

        self.bet_amount = {player: 0.0 for player in self.players}
        self.bet_type = {player: None for player in self.players}
        self.payout = {player: 0.0 for player in self.players}
        self.wheel = Wheel()

    def record_bet(self, player: CustomUser, amount: float, bet_type: dict) -> bool:
        """
            Takes a player and the amount and the type of bet they're betting and recording it in the respective
            dictionaries. Will check if it's a valid bet before recording the bet and return if the recording is successful
            Will set the wheel stage to be ready if all players are ready
            Args:
                player - a CustomUser in the session
                amount - bet amount
                bet_type - the bet type and corresponding arguments, keys of 'type' and optionally 'nums'

            Returns:
                boolean value if the record is successful
        """
        if Roulette.check_bet_valid(bet_type):
            self.bet_amount[player] = amount
            self.bet_type[player] = bet_type
            if self.all_ready():
                self.wheel.stage = 'ready'
            return True
        return False

    @staticmethod
    def check_bet_valid(bet_type: dict) -> bool:
        """
            Checks if bet_type is a valid bet
            Args:
                bet_type - a dict with key type and optionally nums
            Returns:
                boolean value of whether bet is valid
        """
        return bet_type['type'] in ['snake', 'even', 'odd', 'low', 'high', 'basket', 'red', 'black'] or \
               (bet_type['type'] in Bets.BET_CHECKER and Bets.BET_CHECKER[bet_type['type']](bet_type))

    def reset(self):
        """
            Resets the roulette session by wiping all the records clean
        """
        self.wheel = Wheel()
        for player in self.players:
            self.bet_amount[player] = 0
            self.bet_type[player] = None
            self.payout[player] = 0

    def remove_player(self, player: CustomUser):
        """
            Removes a player from the session
            Args:
                player - a CustomerUser in the session
            
        """
        if player in self.players:
            self.bet_amount.pop(player)
            self.bet_type.pop(player)
            self.payout.pop(player)
            self.players.remove(player)
            if len(self.players) == 0:
                self.reset()

    def add_player(self, player: CustomUser):
        """
            Adds a new player to the session
            Args:
                player - the CustomerUser to be added
        """
        if player not in self.players:
            self.players.add(player)
            self.bet_amount[player] = 0.0
            self.bet_type[player] = None
            self.payout[player] = 0.0

    def all_ready(self) -> bool:
        """
            Checks if all player have made a bet and a bet amount
            
            Returns:
                boolean
        """
        return all(self.bet_amount.values()) and all(self.bet_type.values())

    def start_round(self):
        """
            Checks if everyone is ready and then begin rolling the wheel and record player payouts
        """
        if self.all_ready():
            self.wheel.stage = 'ready'
        self.wheel.roll()
        self.find_payout()
        self.player_payout()

    def find_payout(self):
        """
            If the wheel has been spun, calculate the payout for everyone including winners and losers
        """
        if self.wheel.stage == 'ending':
            for player in self.payout:
                self.payout[player] = self.wheel.payout(self.bet_amount[player], self.bet_type[player])

    def player_payout(self):
        """
            Updates each user's balance according to their payout
        """
        for player in self.payout:
            player.update_balance(self.payout[player] - self.bet_amount[player])

    def dict_representation(self) -> dict:
        """
            Returns a dictionary representation of players, bet types, amount, payout, and the wheel dictionary representation

            Returns:
                A dictionary of the game representation
        """
        wheel_dict = self.wheel.dict_representation()
        return {'players': [{'player': player.username,
                             'amount': str(self.bet_amount[player]),
                             'bet': dumps(self.bet_type[player]),
                             'payout': str(self.payout[player])
                             } for player in self.players]

                } | wheel_dict
