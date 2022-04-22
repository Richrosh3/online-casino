from decimal import Decimal

from games.blackjack.game.utils import BlackjackHand, Dealer


class Round:
    def __init__(self, pack, game_instance):
        self.game_instance = game_instance
        self.hands = {player: BlackjackHand() for player in game_instance.players}
        self.round_over = False
        self.pack = pack
        self.dealer = Dealer(pack)
        self.initialize_hand()

    def initialize_hand(self):
        for _ in range(2):
            for hand in list(self.hands.values()) + [self.dealer]:
                hand.hand.append(self.pack.deal())
        self.check_for_blackjack()

    def check_for_blackjack(self):
        for player in self.game_instance.players:
            if self.hands[player].value() == 21:
                self.game_instance.players_ready[player] = True
                self.check_dealers_turn()

    def check_dealers_turn(self):
        if self.get_stage() == 'dealing' and all(self.game_instance.players_ready.values()):
            for player in self.game_instance.players_ready:
                self.game_instance.players_ready[player] = False

            self.play_dealer()

    def make_player_ready(self, player):
        self.game_instance.players_ready[player] = True
        self.check_dealers_turn()

    def update_game(self, player, action):
        if action == 'hit':
            if self.hands[player].hit(self.pack.deal()):
                self.make_player_ready(player)

        elif action == 'stay':
            self.make_player_ready(player)

    def remove_player(self, player):
        self.hands.pop(player)
        self.check_dealers_turn()

    def play_dealer(self):
        self.dealer.play_hand()
        for player, hand in self.hands.items():
            hand.calculate_outcome(self.dealer)
            self.payout_hand(player, hand)
        self.pack.check_reshuffle()
        self.round_over = True

    def payout_hand(self, player, hand):
        if hand.outcome == 'Blackjack':
            player.update_balance(Decimal(2.5) * self.game_instance.bets[player])
        elif hand.outcome == 'Win' or hand.outcome == 'Dealer Bust':
            player.update_balance(2 * self.game_instance.bets[player])
        elif hand.outcome == 'Push':
            player.update_balance(self.game_instance.bets[player])

    def get_stage(self):
        return 'ending' if self.round_over else 'dealing'

    def dict_representation(self, players):
        return {'hands': [{'player': player.username,
                           'hand': self.hands[player].to_list(),
                           'value': self.hands[player].value(),
                           'outcome': self.hands[player].outcome,
                           'ready': self.game_instance.players_ready[player]}
                          for player in players],
                'dealer': {'hand': self.dealer.to_list() if self.round_over else [str(self.dealer.hand[0]), '2B'],
                           'value': self.dealer.value() if self.round_over else self.dealer.hand[0].value
                           }
                }
