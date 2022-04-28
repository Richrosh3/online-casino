from collections import Counter, deque
from decimal import Decimal
from itertools import groupby
from uuid import UUID

from accounts.models import CustomUser
from games.base import Game
from games.poker.game.util import PokerCard
from utils.PlayingCards.deck import Deck

HAND_TYPE_MAPPER = {1: "High Card", 2: 'One Pair', 3: 'Two Pair', 4: 'Three of a Kind', 5: 'Straight', 6: 'Flush',
                    7: 'Full House', 8: 'Four of a Kind', 9: 'Straight Flush'}


class PokerHand:
    def __init__(self, player, hand, board):
        self.hand = hand
        self.stake = 0
        self.folded = False
        self.board = board
        self.player = player

    def dict_representation(self, hide_cards=False):
        self.player.refresh_from_db()
        return {'hand': [str(card) for card in self.hand] if not hide_cards else ["2B" for _ in self.hand],
                'stake': self.stake,
                'folded': self.folded,
                'balance': float(self.player.current_balance) if not hide_cards else None
                }

    def get_cards(self):
        return self.hand + self.board

    def value(self) -> tuple[str, int]:
        return self.check_straight_flush()

    def rank_frequency(self):
        return Counter([card.val for card in self.get_cards()])

    def suit_frequency(self):
        return Counter([card.suit.suit for card in self.get_cards()])

    @staticmethod
    def hand_value(playable_hand: list, hand_type: int) -> tuple[str, int]:
        value = str(hand_type)

        for card in playable_hand:
            value += "{:02d}".format(card)
        return HAND_TYPE_MAPPER[hand_type], int(value)

    def check_straight_flush(self) -> tuple[str, int]:
        """
        Checks if hand is a straight flush
        Returns: int representation of the hand
        """
        suit_counts = self.suit_frequency()
        five_of_same_suit = [key for key, value in suit_counts.items() if value >= 5]
        if len(five_of_same_suit) > 0:
            same_suit = [card for card in self.get_cards() if card.suit == five_of_same_suit[0]]
            card_values = [card.val for card in same_suit]
            consecutive_cards = self.get_five_or_more_consecutive_cards(card_values)
            if len(consecutive_cards) > 0:
                return self.hand_value(sorted(consecutive_cards[0], reverse=True)[:5], 9)

            # Replacing the value of any Aces to 1 to see if there are any straights with it as a 1
            if 14 in card_values:
                card_values = [1 if rank == 14 else rank for rank in card_values]
                consecutive_cards = self.get_five_or_more_consecutive_cards(card_values)
                if len(consecutive_cards) > 0:
                    return self.hand_value(sorted(consecutive_cards[0], reverse=True)[:5], 9)

        return self.check_four_of_a_kind()

    def check_four_of_a_kind(self) -> tuple[str, int]:
        """
        Checks if hand is a four of a kind
        Returns: int representation of the hand
        """
        counts = self.rank_frequency()
        if 4 in counts.values():
            four_rank = [rank for rank, count in counts.items() if count == 4][0]
            four_of_a_kind = [four_rank for _ in range(4)]
            playable_hand = four_of_a_kind + sorted((counts - Counter(four_of_a_kind)).elements(), reverse=True)[:1]
            return self.hand_value(playable_hand, 8)

        return self.check_full_house()

    def check_full_house(self) -> tuple[str, int]:
        """
        Checks if hand is a full house
        Returns: int representation of the hand
        """
        counts = self.rank_frequency()

        frequency_of_three_or_more = [key for key, value in counts.items() if value >= 3]
        if len(frequency_of_three_or_more) > 0:
            three_rank = sorted(frequency_of_three_or_more)[-1]
            three_of_a_kind = [three_rank for _ in range(3)]
            counts_left = counts - Counter(three_of_a_kind)

            frequency_of_two_or_more = [key for key, value in counts_left.items() if value >= 2]
            if len(frequency_of_two_or_more) > 0:
                pair_rank = sorted(frequency_of_two_or_more)[-1]
                pair_cards = [pair_rank for _ in range(2)]

                return self.hand_value(three_of_a_kind + pair_cards, 7)

        return self.check_flush()

    def check_flush(self) -> tuple[str, int]:
        """
        Checks if the hand is a flush
        Returns: int representation of the hand
        """
        suit_counts = self.suit_frequency()
        five_of_same_suit = [key for key, value in suit_counts.items() if value >= 5]
        if len(five_of_same_suit) > 0:
            same_suit = [card.val for card in self.get_cards() if card.suit == five_of_same_suit[0]]
            return self.hand_value(sorted(same_suit, reverse=True)[:5], 6)

        return self.check_straight()

    @staticmethod
    def get_five_or_more_consecutive_cards(ranks: list) -> list:
        """
        Returns a list of 5+ cards if they are all consecutive
        Args:
            ranks: list of ranks to be checked

        Returns:
            List of lists that contain the consecutive streaks
        """
        ranks = sorted(ranks)
        grpby = groupby(enumerate(ranks), key=lambda x: x[0] - x[1])
        all_groups = ([rank[1] for rank in group] for _, group in grpby)
        return list(filter(lambda x: len(x) >= 5, all_groups))

    def check_straight(self) -> tuple[str, int]:
        """
        Checks if the hand is a straight, can either be with Ace as the highest card or
        with Ace representing a 1 for the lowest straight possible of A, 2, 3, 4, 5
        Returns: int representation of the hand
        """
        card_values = [card.val for card in self.get_cards()]
        consecutive_cards = self.get_five_or_more_consecutive_cards(card_values)
        if len(consecutive_cards) > 0:
            return self.hand_value(sorted(consecutive_cards[0], reverse=True)[:5], 5)

        # Replacing the value of any Aces to 1 to see if there are any straights with it as a 1
        if 14 in card_values:
            card_values = [1 if rank == 14 else rank for rank in card_values]
            consecutive_cards = self.get_five_or_more_consecutive_cards(card_values)
            if len(consecutive_cards) > 0:
                return self.hand_value(sorted(consecutive_cards[0], reverse=True)[:5], 5)

        return self.check_three_of_a_kind()

    def check_three_of_a_kind(self) -> tuple[str, int]:
        """
        Checks if a hand is a 3 of a kind
        Returns: int representation of the hand
        """
        counts = self.rank_frequency()

        frequency_of_three_or_more = [key for key, value in counts.items() if value >= 3]
        if len(frequency_of_three_or_more) > 0:
            three_rank = sorted(frequency_of_three_or_more)[-1]
            three_of_a_kind = [three_rank for _ in range(3)]
            counts_left = counts - Counter(three_of_a_kind)
            playable_hand = three_of_a_kind + sorted(counts_left.elements(), reverse=True)[:2]

            return self.hand_value(playable_hand, 4)

        return self.check_two_pairs()

    def check_two_pairs(self) -> tuple[str, int]:
        """
        Checks if a card is a two pair
        Returns: int representation of the hand
        """
        counts = self.rank_frequency()
        frequency_of_two_or_more = [key for key, value in counts.items() if value >= 2]
        if len(frequency_of_two_or_more) >= 2:
            pair_ranks = sorted(frequency_of_two_or_more, reverse=True)[:2]
            pairs_cards = [pair_ranks[0] for _ in range(2)] + [pair_ranks[1] for _ in range(2)]
            playable_hand = pairs_cards + sorted((counts - Counter(pairs_cards)).elements(), reverse=True)[:1]
            return self.hand_value(playable_hand, 3)

        return self.check_one_pair()

    def check_one_pair(self) -> tuple[str, int]:
        """
        checks if the hand contains a pair
        Returns: int representation of the hand
        """
        counts = self.rank_frequency()
        frequency_of_two_or_more = [key for key, value in counts.items() if value >= 2]
        if len(frequency_of_two_or_more) > 0:
            pair_rank = sorted(frequency_of_two_or_more, reverse=True)[0]
            pairs_cards = [pair_rank for _ in range(2)]
            counts_left = counts - Counter(pairs_cards)

            playable_hand = pairs_cards + sorted(counts_left.elements(), reverse=True)[:3]
            return self.hand_value(playable_hand, 2)

        return self.check_high_card()

    def check_high_card(self) -> tuple[str, int]:
        """
        Returns the high cards
        Returns: int representation of the hand
        """
        card_values = [card.val for card in self.get_cards()]
        highest_five_cards = sorted(card_values, reverse=True)[:5]
        return self.hand_value(highest_five_cards, 1)

    def __lt__(self, other):
        return self.value() < other.value()

    def __le__(self, other):
        return self.value() <= other.value()

    def __eq__(self, other):
        return self.value() == other.value()

    def __ne__(self, other):
        return self.value() != other.value()

    def __gt__(self, other):
        return self.value() > other.value()

    def __ge__(self, other):
        return self.value() >= other.value()


class PokerRound:
    def __init__(self, deck, players) -> None:
        self.hands = dict()
        self.players_in_hand = deque(players)
        self.last_raiser = self.players_in_hand[0]
        self.round_over = False
        self.board = []
        self.pot = 0.0
        self.price_to_call = 0
        self.deck = deck
        self.outcomes = {}
        self.winners = []
        self.deal_cards()

    def remove_player(self, player):
        if player in self.players_in_hand and not self.round_over:
            if self.last_raiser == player:
                player_before = self.players_in_hand[
                    (self.players_in_hand.index(player) + len(self.players_in_hand) - 1) % len(self.players_in_hand)]
                self.last_raiser = player_before
                self.price_to_call = self.hands[player_before].stake

            self.players_in_hand.remove(player)

            self.outcomes[player] = "Player Left"

            self.check_round_end()

    def deal_cards(self):
        """
            Shuffles and deals cards to everyone sitting down at the table, starting the new round
            parameters: None
            Returns: None
        """

        for player in self.players_in_hand:
            self.hands[player] = PokerHand(player, self.deck.deal(2), self.board)

    def evaluate_winner(self) -> None:
        """
        Evaluates all hands among each of the players that haven't folded and determines who won
        parameters: a 5 card hand
        Returns: a list comprising of the best rank of the hand, its kickers, and the hand itself
        """
        outcomes = {}
        winners = []
        best_score = 0

        for player in self.players_in_hand:
            if not self.hands[player].folded:
                hand_type, hand_value = self.hands[player].value()
                outcomes[player] = hand_type
                if hand_value == best_score:
                    winners.append(player)
                elif hand_value > best_score:
                    winners = [player]
                    best_score = hand_value

        self.winners = winners
        self.outcomes = outcomes
        self.round_over = True

        for winner in winners:
            winner.update_balance(Decimal(self.pot / len(winners)))

    def update_board(self) -> None:
        """
        Updates the board with the next card or evaluates the winner
        parameters: None
        Returns: None
        """

        cards_dealt = len(self.board)

        if cards_dealt == 0:
            self.board += self.deck.deal(3)
        elif cards_dealt == 3 or cards_dealt == 4:
            self.board += self.deck.deal(1)
        elif cards_dealt == 5:
            self.reset_stakes()
            self.evaluate_winner()

    def reset_stakes(self) -> None:
        """
        updates the stakes of the players in the hand
        """
        for player in self.players_in_hand:
            self.pot += self.hands[player].stake
            self.hands[player].stake = 0

        self.price_to_call = 0

    def end_round(self) -> None:
        """
        Ends the current round after the board has circled around to the last raiser when the action is closed
        Parameters: Request containing the CustomUser
        Returns: None
        """
        self.reset_stakes()
        self.update_board()

    def player_action(self, player: CustomUser, action: str, bet: float) -> None:
        """
        Whenever a player makes a move, will update if it is the users turn. When the
        current turn passes the last player to act, it will end the turn to close the action
        parameters: a dictionary containing the action to bet, fold or call/check
            bet: {"Action": "bet", "amount": 20.0, "player": CustomUser(uuid())}
            call: {"Action": "call", "player": CustomUser(uuid())}
            Fold: {"Action": "fold", "player": CustomUser(uuid())}
        Returns: Nothing
        """

        if player != self.players_in_hand[0]:
            return

        if action == "bet":
            if bet <= self.price_to_call:
                return
            self.player_bet(player, bet)
        elif action == "call" or action == "check":
            self.player_call(player)
        elif action == "fold":
            self.hands[player].folded = True
            self.players_in_hand.remove(player)

        self.check_round_end()

    def check_round_end(self):
        if len(self.players_in_hand) == 1:
            self.reset_stakes()
            self.winners = [self.players_in_hand[0]]
            self.round_over = True

        elif self.players_in_hand[0] == self.last_raiser:
            self.end_round()

    def change_turn(self) -> None:
        """
        Moves the current turn to the next user in line that hasn't folded or
        is the last person to raise to close action
        parameters: None
        Returns: None
        """
        self.players_in_hand.rotate(-1)

    def player_bet(self, player: CustomUser, bet: float) -> None:
        """
        request contains the bet amount (float), and player, increases the price to call
        parameters: a dictionary containing the action to bet, fold or call/check
            bet: {"Action": "bet", "amount": 20.0, "player": CustomUser(uuid())}
            call: {"Action": "call", "player": CustomUser(uuid())}
            Fold: {"Action": "fold", "player": CustomUser(uuid())}
        Returns: Nothing
        """

        if self.price_to_call <= bet <= player.current_balance:
            self.price_to_call = self.hands[player].stake + bet
            self.last_raiser = self.players_in_hand[0]
            self.hands[player].stake += bet
            player.update_balance(-1 * Decimal(bet))
            self.change_turn()

    def player_call(self, player: CustomUser) -> None:
        """
        The user has decided to make the call or check
        parameters: a dictionary containing the action to bet, fold or call/check
            bet: {"Action": "bet", "amount": 20.0, "player": CustomUser(uuid())}
            call: {"Action": "call", "player": CustomUser(uuid())}
            Fold: {"Action": "fold", "player": CustomUser(uuid())}
        Returns: Nothing
        """

        if self.price_to_call <= player.current_balance:
            player.update_balance(-1 * Decimal(self.price_to_call - self.hands[player].stake))
            self.hands[player].stake = self.price_to_call
            self.change_turn()

    def dict_representation(self, user: CustomUser) -> dict:
        """
        Returns a dictionary representation of the poker session data,
        used for web application when we want to get some information about the
        poker game
        parameters: None
        Returns: dictionary containing information about the poker session
        """

        return {"stage": 'ending' if self.round_over else 'playing',
                "game": {"pot": self.pot,
                         "price_to_call": self.price_to_call,
                         "current_turn": self.players_in_hand[0].username if not self.round_over else None,
                         "board": [str(card) for card in self.board],
                         "winners": [winner.username for winner in self.winners],
                         "outcomes": {player.username: player_outcome for player, player_outcome in
                                      self.outcomes.items()}},
                "players": {player.username: self.hands[player].dict_representation(
                    hide_cards=((player != user) and not self.round_over)) for player in self.hands}
                }


class Poker(Game):
    def __init__(self, session_id: UUID):
        super().__init__(session_id)
        self.round = None
        self.players_ready = dict()
        self.deck = Deck(PokerCard)

    def add_player(self, player: CustomUser) -> None:
        """
        Adds a player to the game
        Args:
            player: player to be added
        """
        self.players.add(player)
        self.players_ready[player] = False

    def remove_player(self, player: CustomUser) -> None:
        """
        Adds a player to the game
        Args:
            player: player to be added
        """
        if player in self.players:
            self.players.remove(player)
        if player in self.players_ready:
            self.players_ready.pop(player)
        if self.round is not None:
            self.round.remove_player(player)

        self.check_move_to_next_stage()

    def reset(self):
        self.deck.build()
        self.deck.shuffle()
        self.players_ready = {player: False for player in self.players}
        if len(self.players) > 1:
            self.start_round()
        else:
            self.round = None

    def start_round(self):
        self.round = PokerRound(self.deck, self.players)

    def check_move_to_next_stage(self):
        if all(self.players_ready.values()):
            if self.round is not None:
                self.reset()

            elif len(self.players) > 1:
                self.players_ready = {player: False for player in self.players}
                self.start_round()

    def ready_up(self, player, ready_state):
        self.players_ready[player] = ready_state
        self.check_move_to_next_stage()

    def dict_representation(self, user: CustomUser):
        if self.round is not None:
            return self.round.dict_representation(user) | {
                'players_ready': {player.username: player_ready for player, player_ready in self.players_ready.items()}}
        else:
            return {'stage': 'waiting',
                    'players_ready': {player.username: player_ready for player, player_ready in
                                      self.players_ready.items()}
                    }
