from games.poker.game.util import PokerCard
from utils.PlayingCards.deck import Deck
from uuid import UUID, uuid4
from games.base import Game
from accounts.models import CustomUser


class Poker(Game):
    def __init__(self, session_id: UUID) -> None:
        super().__init__(session_id)
        self.players = list()
        self.in_limbo = set()
        self.board = list()
        self.pot = 0.0
        self.players_info = dict()
        self.deck = Deck(PokerCard)
        self.deck.build()
        self.players_in_hand = 0
        self.dealer_index = 0
        self.price_to_call = 0.0
        self.last_raiser = 0
        self.current_turn = 0

    def add_player(self, player: CustomUser):
        """
        Adds players to the list one by one

        parameters: CustomUser
        Returns: None
        """
        self.players.append(player)

    def reset_board(self):
        self.deck.build()
        self.deck.shuffle()
        self.board = []
        self.dealer_index = (self.dealer_index + 1) % len(self.players)
        self.players_in_hand = len(self.players)
        self.current_turn = (self.dealer_index + 1) % len(self.players)
        self.last_raiser = self.current_turn

    def deal_cards(self):
        """
            Shuffles and deals cards to everyone sitting down at the table, starting the new round
            parameters: None
            Returns: None
        """
        self.reset_board()

        for player in self.players:
            self.players_info[player] = dict()
            self.players_info[player]["hand"] = [self.deck.deck.pop(), self.deck.deck.pop()]
            self.players_info[player]["stake"] = 0.0
            self.players_info[player]["folded"] = False

    def check_straight_flush(self, hand: list) -> list:
        """
        checks if user has a straight flush
        parameters: a 5 card hand
        Returns: list of cards needed to determine kicker
        """
        if self.check_flush(hand) and self.check_straight(hand):
            card_values = [card.val for card in hand]
            return [sorted(card_values)[5]]
        return []

    @staticmethod
    def check_straight_flush_kickers(hand_1: list, hand_2: list) -> list:
        if hand_1[0] > hand_2[0]:
            return hand_1[0]
        return hand_2[0]

    @staticmethod
    def check_four_of_a_kind(hand: list) -> list:
        """
        checks if hand is a four of a kind
        parameters: a 5 card hand
        Returns: list of cards needed to determine kicker
        """
        card_values = [card.val for card in hand]
        value_counts = {}
        for card in card_values:
            if value_counts.__contains__(card):
                value_counts[card] += 1
            else:
                value_counts[card] = 1

        if sorted(value_counts.values()) == [1, 4]:
            keys = list(value_counts.keys())
            if value_counts[keys[0]] == 1:
                return keys
            return [keys[1], keys[0]]

        return False

    @staticmethod
    def check_four_of_a_kind_kickers(hand_1: list, hand_2: list) -> list:
        if hand_1[1] > hand_2[1]:
            return hand_1
        else:
            return hand_2

    @staticmethod
    def check_full_house(hand: list) -> list:

        """
        Returns the full house combo if possible in the form [2 of a kind, 3 of a kind] for the combination of the hand
        that makes up the full house
        """
        card_values = [card.val for card in hand]
        value_counts = {}
        for card in card_values:
            if value_counts.__contains__(card):
                value_counts[card] += 1
            else:
                value_counts[card] = 1

        sorted_value_counts = sorted(value_counts.values())

        if sorted_value_counts == [2, 3]:
            keys = list(value_counts.keys())
            if value_counts[keys[0]] == 2:
                return keys
            return [keys[1], keys[0]]

        return []

    @staticmethod
    def check_full_house_kickers(hand_1: list, hand_2: list) -> list:
        if hand_1[1] > hand_2[1]:
            return hand_1
        elif hand_1[1] < hand_2[1]:
            return hand_2
        else:
            if hand_1[0] > hand_2[0]:
                return hand_1
            else:
                return hand_2

    @staticmethod
    def check_flush(hand: list) -> list:
        """
        checks if the hand is a flush
        parameters: a 5 card hand
        Returns: list of cards needed to determine kicker
        """
        suits = [str(card.suit) for card in hand]
        if len(set(suits)) == 1:
            return [sorted([card.val for card in hand])[4]]
        else:
            return []

    @staticmethod
    def check_flush_kickers(hand_1: list, hand_2: list):
        if hand_1[0] > hand_2[0]:
            return hand_1
        return hand_2

    @staticmethod
    def check_straight(hand: list) -> list:
        """
        checks if the hand is a straight, can either be with Ace as the highest card or
        with Ace representing a 1 for the lowest straight possible of A, 2, 3, 4, 5
        parameters: a 5 card hand
        Returns: list of cards needed to determine kicker
        """
        card_values = [card.val for card in hand]

        if len(set(card_values)) == 5:
            sorted_card_values = sorted(card_values)
            if sorted_card_values[4] == 14 and sorted_card_values[3] == 5:
                return [5]
            elif sorted_card_values[4] - sorted_card_values[0] == 4:
                return [sorted_card_values[4]]
        return []

    @staticmethod
    def check_straight_kickers(hand_1: list, hand_2: list) -> list:
        if hand_1[0] > hand_2[0]:
            return hand_1
        return hand_2

    @staticmethod
    def check_three_of_a_kind(hand: list) -> list:
        """
        checks if a hand is a 3 of a kind
        parameters: a 5 card hand
        Returns: list of cards needed to determine kicker
        """
        card_values = [card.val for card in hand]
        value_counts = {}
        for card in card_values:
            if value_counts.__contains__(card):
                value_counts[card] += 1
            else:
                value_counts[card] = 1

        if set(value_counts.values()) == set([3, 1]):
            return sorted({key: val for key, val in value_counts.items() if val != 3}.keys())

        return []

    @staticmethod
    def check_three_of_a_kind_kicker(hand_1: list, hand_2: list) -> list:
        if hand_1[1] > hand_2[1]:
            return hand_1
        elif hand_1[1] < hand_2[1]:
            return hand_2
        else:
            if hand_1[0] > hand_2[0]:
                return hand_1
            return hand_2

    @staticmethod
    def check_two_pairs(hand: list) -> list:
        """
        Checks if a card is a two pair
        parameters: a 5 card hand
        Returns: list of cards needed to determine kicker
        """
        card_values = [card.val for card in hand]
        value_counts = {}
        for card in card_values:
            if value_counts.__contains__(card):
                value_counts[card] += 1
            else:
                value_counts[card] = 1
        if sorted(value_counts.values()) == [1, 2, 2]:
            return sorted({key: val for key, val in value_counts.items() if val != 1}.keys())
        else:
            return []

    @staticmethod
    def check_two_pair_kicker(hand_1: list, hand_2: list) -> list:
        if hand_1[1] > hand_2[1]:
            return hand_1
        elif hand_1[1] < hand_2[1]:
            return hand_2
        else:
            if hand_1[0] > hand_2[0]:
                return hand_1
            else:
                return hand_2

    @staticmethod
    def check_one_pairs(hand: list) -> list:
        """
        checks if the hand contains a pair
        parameters: a 5 card hand
        Returns: list of cards needed to determine kicker
        """
        card_values = [card.val for card in hand]
        value_counts = {}
        pair = -1
        for card in card_values:
            if value_counts.__contains__(card):
                value_counts[card] += 1
                pair = card
            else:
                value_counts[card] = 1

        if 2 in value_counts.values():
            return sorted({key: val for key, val in value_counts.items() if val != 2}.keys()) + [pair]
        else:
            return []

    @staticmethod
    def check_one_pair_kicker(hand_1: list, hand_2: list) -> list:
        if hand_1[3] > hand_2[3]:
            return hand_1
        return hand_2

    @staticmethod
    def check_high_card(hand: list) -> list:
        """
        Returns the high card on the board to determine kickers
        parameters: a 5 card hand
        Returns: list of cards needed to determine kicker
        """
        card_values = [card.val for card in hand]
        return [max(card_values)]

    def get_possible_hands(self, hand: list) -> list:
        """
        returns a list of all total possible 5 card hands from the set of 7 cards (5 on the board
        and 2 that the player is holding)
        parameters: a 5 card hand
        Returns: list of cards needed to determine kicker
        """
        combined_hand = self.board + hand
        possible_hands = []

        for first_missing in range(0, 6):
            for second_missing in range(first_missing + 1, 7):
                five_card_hand = combined_hand[0:first_missing] + combined_hand[first_missing + 1:second_missing]
                five_card_hand += combined_hand[second_missing + 1:]

                possible_hands.append(five_card_hand)

        return possible_hands

    def find_best_hand(self, possible_hands: list) -> list:

        """
        Determines what the best possible hand out of all the possible hands passed in
        Ranks: No pair: 0, Pair: 1, Two Pair: 2, Set/Trips: 3, straight: 4, flush: 5, Full house: 6,
        Quads:7, Straight flush: 8
        parameters: a 5 card hand
        Returns: a list comprising of the best rank of the hand, its kickers, and the hand itself
        """

        best = [-1, [], []]

        for hand in possible_hands:
            result = [8, self.check_straight_flush(hand), hand]
            if result[1]:
                if result[0] > best[0] or self.check_straight_flush_kickers(result[1], best[1]):
                    best = result
                continue

            result = [7, self.check_four_of_a_kind(hand), hand]
            if result[1]:
                if result[0] > best[0] or (
                        result[0] == best[0] and self.check_four_of_a_kind_kickers(result[1], best[1])):
                    best = result
                continue

            result = [6, self.check_full_house(hand), hand]
            if result[1]:
                if result[0] > best[0] or (result[0] == best[0] and self.check_full_house_kickers(result[1], best[1])):
                    best = result
                continue

            result = [5, self.check_flush(hand), hand]
            if result[1]:
                if result[0] > best[0] or (result[0] == best[0] and self.check_flush_kickers(result[1], best[1])):
                    best = result
                continue

            result = [4, self.check_straight(hand), hand]
            if result[1]:
                if result[0] > best[0] or (result[0] == best[0] and self.check_straight_kickers(result[1], best[1])):
                    best = result
                continue

            result = [3, self.check_three_of_a_kind(hand), hand]
            if result[1]:
                if result[0] > best[0] or (
                        result[0] == best[0] and self.check_three_of_a_kind_kicker(result[1], best[1])):
                    best = result
                continue

            result = [2, self.check_two_pairs(hand), hand]
            if result[1]:
                if result[0] > best[0] or (result[0] == best[0] and self.check_two_pair_kicker(result[1], best[1])):
                    best = result
                continue

            result = [1, self.check_one_pairs(hand), hand]
            if result[1]:
                if result[0] > best[0] or (result[0] == best[0] and self.check_one_pair_kicker(result[1], best[1])):
                    best = result
                continue

            result = [0, self.check_high_card(hand), hand]
            if result[0] > best[0] and result[1] > best[1]:
                best = result
                continue

        return best

    def update_winner_status(self) -> None:
        """
        Gives all money in the pot to the winner
        """
        self.reset_stakes()
        return

    def evaluate_winner(self) -> str:
        """
        Evaluates all hands among each of the players that haven't folded and determines who won
        parameters: a 5 card hand
        Returns: a list comprising of the best rank of the hand, its kickers, and the hand itself
        """
        possible_hands = dict()

        total_hands = []
        for player in self.players_info:
            if not self.players_info[player]["folded"]:
                player_hands = self.get_possible_hands(self.players_info[player]["hand"])
                possible_hands[player] = player_hands
                total_hands += player_hands

        best_hand = self.find_best_hand(total_hands)

        print(best_hand)
        for player in possible_hands:
            if possible_hands[player].__contains__(best_hand[2]):
                return player
        return -1

    def update_board(self) -> None:
        """
        Updates the board with the next card or evaluates the winner
        parameters: None
        Returns: None
        """,

        cards_dealt = len(self.board)

        if cards_dealt == 0:
            for _ in range(0, 3):
                card = self.deck.deck.pop()
                print(card.__str__())
                self.board.append(card)
        elif cards_dealt == 3:
            self.board.append(self.deck.deck.pop())
        elif cards_dealt == 4:
            self.board.append(self.deck.deck.pop())
        elif cards_dealt == 5:
            self.evaluate_winner()
            self.update_winner_status()
            return

    def reset_stakes(self) -> None:
        """
        updates the stakes of the players in the hand

        """
        for player in self.players_info:
            self.pot += self.players_info[player]["stake"]
            self.players_info[player]["stake"] = 0

        self.price_to_call = 0

    def end_round(self) -> None:
        """
        Ends the current round after the board has circled around to the last raiser when the action is closed
        Parameters: Request containing the CustomUser
        Returns: None
        """
        self.reset_stakes()
        self.update_board()

        self.current_turn = self.dealer_index
        self.get_next_turn()
        self.last_raiser = self.current_turn

    def player_action(self, request: dict) -> None:
        """
        Whenever a player makes a move, will update if it is the users turn. When the
        current turn passes the last player to act, it will end the turn to close the action
        parameters: a dictionary containing the action to bet, fold or call/check
            bet: {"Action": "bet", "amount": 20.0, "player": CustomUser(uuid())}
            call: {"Action": "call", "player": CustomUser(uuid())}
            Fold: {"Action": "fold", "player": CustomUser(uuid())}
        Returns: Nothing
        """
        # also check if the player exists
        # if self.players.index(player) != self.current_turn:
        # return

        if request["action"] == "bet":
            self.player_bet(request)
        elif request["action"] == "call" or request["action"] == "check":
            self.player_call(request)
        elif request["action"] == "fold":
            self.player_fold(request)

    def get_next_turn(self) -> None:
        """
        Moves the current turn to the next user in line that hasn't folded or
        is the last person to raise to close action
        parameters: None
        Returns: None
        """

        self.current_turn = (self.current_turn + 1) % len(self.players)

        # checks if the player has folded or if the current player is the last to act
        while self.players_info[self.players[self.current_turn]]["folded"] and self.current_turn != self.last_raiser:
            self.current_turn = (self.current_turn + 1) % len(self.players)

    def player_bet(self, request: dict) -> None:
        """
        request contains the bet amount (float), and player, increases the price to call
        parameters: a dictionary containing the action to bet, fold or call/check
            bet: {"Action": "bet", "amount": 20.0, "player": CustomUser(uuid())}
            call: {"Action": "call", "player": CustomUser(uuid())}
            Fold: {"Action": "fold", "player": CustomUser(uuid())}
        Returns: Nothing
        """
        bet = request["amount"]
        player = request["player"]

        if self.players.index(player) != self.current_turn:
            return

        # Check if bet > stake
        self.price_to_call = bet
        self.last_raiser = self.current_turn
        self.players_info[player]["stake"] = bet
        self.get_next_turn()

    def player_call(self, request: dict) -> None:
        """
        The user has decided to make the call or check
        parameters: a dictionary containing the action to bet, fold or call/check
            bet: {"Action": "bet", "amount": 20.0, "player": CustomUser(uuid())}
            call: {"Action": "call", "player": CustomUser(uuid())}
            Fold: {"Action": "fold", "player": CustomUser(uuid())}
        Returns: Nothing
        """

        player = request["player"]

        if self.players.index(player) != self.current_turn:
            return
        self.players_info[player]["stake"] = self.price_to_call
        self.get_next_turn()

    def player_fold(self, request: dict) -> None:
        """
        The player folds, decreasing players in hand
        parameters: a dictionary containing the action to bet, fold or call/check
            bet: {"Action": "bet", "amount": 20.0, "player": CustomUser(uuid())}
            call: {"Action": "call", "player": CustomUser(uuid())}
            Fold: {"Action": "fold", "player": CustomUser(uuid())}
        Returns: Nothing
        """
        player = request["player"]

        if self.players.index(player) != self.current_turn:
            return

        self.players_info[player]["folded"] = True
        self.get_next_turn()
        self.players_in_hand -= 1

    def dict_representation(self) -> dict:
        game_data = {"pot": self.pot, "player_info": self.players_info,
                     "dealer_index": self.dealer_index, "current_turn": self.players[self.current_turn],
                     "board": self.board}

        return game_data
