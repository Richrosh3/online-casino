from uuid import uuid4
from django.test import TestCase
import unittest
from games.base import Game
from games.poker.game.poker import Poker
from accounts.models import CustomUser
from games.poker.game.util import PokerCard

class PokerGameTestDeal(unittest.TestCase):
    def test_add_player_adds_player(self):
        session = Poker(Game(uuid4()))
        user = CustomUser()
        user.username = "andrew"
        session.add_player(user)
        self.assertEqual(session.players, [user.username])

    def test_add_player_doesnt_add_duplicates(self):
        session = Poker(Game(uuid4()))
        user = CustomUser()
        user.username = "andrew"
        session.add_player(user)
        session.add_player(user)
        self.assertEqual(session.players, [user.username])
        self.assertEqual(len(session.players), 1)

    def test_reset_sets_stats(self):
        session = Poker(Game(uuid4()))
        user = CustomUser()
        user.username = "andrew"
        session.players = [user.username, "drew"]
        session.dealer_index = 0
        session.reset_board()

        self.assertEqual(session.board, [])
        self.assertEqual(len(session.deck.deck), 52)
        self.assertEqual(session.pot, 0.0)
        self.assertEqual(session.dealer_index, 1)
        self.assertEqual(session.players_in_hand, 2)
        self.assertEqual(session.current_turn, 0)
        self.assertEqual(session.last_raiser, 0)
        self.assertEqual(session.winner, "")

    def test_deal_cards_deals_to_all_players(self):
        session = Poker(Game(uuid4()))
        user = CustomUser()
        user.username = "andrew"
        session.players = [user.username, "drew"]
        session.dealer_index = 0
        session.deal_cards()
        self.assertEqual(len(session.players_info["andrew"]["hand"]), 2)
        self.assertEqual(len(session.players_info["drew"]["hand"]), 2)
        self.assertEqual(session.players_info["andrew"]["stake"], 0.0)
        self.assertEqual(session.players_info["andrew"]["folded"], False)
        self.assertEqual(session.players_info["drew"]["stake"], 0.0)
        self.assertEqual(session.players_info["drew"]["folded"], False)


class PokerGameTestStraightFlush(unittest.TestCase):
    def test_is_straight_flush(self):
        hand = [PokerCard('S', 10), PokerCard('S', 9), PokerCard('S', 8), PokerCard('S', 7), PokerCard('S', 6)]
        session = Poker(Game(uuid4()))
        self.assertEqual(session.check_straight_flush(hand), [10])

    def test_is_not_straight_flush(self):
        hand = [PokerCard('S', 10), PokerCard('S', 5), PokerCard('S', 8), PokerCard('S', 7), PokerCard('S', 6)]
        session = Poker(Game(uuid4()))
        self.assertEqual(session.check_straight_flush(hand), [])

    def test_kicker_gives_right_hand(self):
        hand1 = [10]
        hand2 = [11]
        session = Poker(Game(uuid4()))
        self.assertEqual(session.check_straight_flush_kickers(hand1, hand2), hand2)


class PokerGameTestQuads(unittest.TestCase):
    def test_is_quads(self):
        hand = [PokerCard('S', 10), PokerCard('D', 10), PokerCard('C', 10), PokerCard('H', 10), PokerCard('S', 6)]
        session = Poker(Game(uuid4()))
        self.assertEqual(session.check_four_of_a_kind(hand), [6, 10])

    def test_is_quads(self):
        hand = [PokerCard('H', 6), PokerCard('D', 10), PokerCard('C', 10), PokerCard('H', 10), PokerCard('S', 6)]
        session = Poker(Game(uuid4()))
        self.assertEqual(session.check_four_of_a_kind(hand), [])

    def test_kicker_gives_right_hand(self):
        hand1 = [6, 10]
        hand2 = [6, 9]
        session = Poker(Game(uuid4()))
        self.assertEqual(session.check_four_of_a_kind_kickers(hand1, hand2), hand1)


class PokerGameTestFullHouse(unittest.TestCase):
    def test_is_full_house(self):
        hand = [PokerCard('S', 10), PokerCard('D', 10), PokerCard('C', 10), PokerCard('H', 6), PokerCard('S', 6)]
        session = Poker(Game(uuid4()))
        self.assertEqual(session.check_full_house(hand), [6, 10])

    def test_is_not_full_house(self):
        hand = [PokerCard('S', 10), PokerCard('D', 10), PokerCard('C', 5), PokerCard('H', 6), PokerCard('S', 6)]
        session = Poker(Game(uuid4()))
        self.assertEqual(session.check_full_house(hand), [])

    def test_kicker_gives_right_hand(self):
        hand1 = [6, 10]
        hand2 = [6, 12]
        session = Poker(Game(uuid4()))
        self.assertEqual(session.check_full_house_kickers(hand1, hand2), hand2)


class PokerGameTestFlush(unittest.TestCase):
    def test_is_flush(self):
        hand = [PokerCard('S', 11), PokerCard('S', 14), PokerCard('S', 10), PokerCard('S', 6), PokerCard('S', 5)]
        session = Poker(Game(uuid4()))
        self.assertEqual(session.check_flush(hand), [14])

    def test_is_not_flush(self):
        hand = [PokerCard('S', 11), PokerCard('D', 14), PokerCard('S', 10), PokerCard('S', 6), PokerCard('S', 5)]
        session = Poker(Game(uuid4()))
        self.assertEqual(session.check_flush(hand), [])

    def test_kicker_gives_right_hand(self):
        hand1 = [10]
        hand2 = [5]
        session = Poker(Game(uuid4()))
        self.assertEqual(session.check_flush_kickers(hand1, hand2), hand1)


class PokerGameTestStraight(unittest.TestCase):
    def test_is_straight(self):
        hand = [PokerCard('S', 11), PokerCard('S', 12), PokerCard('S', 10), PokerCard('D', 8), PokerCard('S', 9)]
        session = Poker(Game(uuid4()))
        self.assertEqual(session.check_straight(hand), [12])

    def test_is_not_straight(self):
        hand = [PokerCard('S', 5), PokerCard('S', 12), PokerCard('S', 10), PokerCard('D', 8), PokerCard('S', 9)]
        session = Poker(Game(uuid4()))
        self.assertEqual(session.check_straight(hand), [])

    def test_kicker_gives_right_hand(self):
        hand1 = [10]
        hand2 = [7]
        session = Poker(Game(uuid4()))
        self.assertEqual(session.check_straight_kickers(hand1, hand2), hand1)


class PokerGameTestTrips(unittest.TestCase):
    def test_is_trips(self):
        hand = [PokerCard('S', 11), PokerCard('D', 11), PokerCard('C', 11), PokerCard('D', 8), PokerCard('S', 9)]
        session = Poker(Game(uuid4()))
        self.assertEqual(session.check_three_of_a_kind(hand), [8, 9, 11])

    def test_is_not_trips(self):
        hand = [PokerCard('S', 12), PokerCard('D', 11), PokerCard('C', 11), PokerCard('D', 8), PokerCard('S', 9)]
        session = Poker(Game(uuid4()))
        self.assertEqual(session.check_three_of_a_kind(hand), [])

    def test_kicker_gives_right_hand(self):
        hand1 = [4, 5, 10]
        hand2 = [4, 5, 7]
        session = Poker(Game(uuid4()))
        self.assertEqual(session.check_three_of_a_kind_kicker(hand1, hand2), hand1)


class PokerGameTestTwoPair(unittest.TestCase):
    def test_is_two_pair(self):
        hand = [PokerCard('S', 11), PokerCard('D', 11), PokerCard('C', 8), PokerCard('D', 8), PokerCard('S', 9)]
        session = Poker(Game(uuid4()))
        self.assertEqual(session.check_two_pairs(hand), [8, 11])

    def test_is_not_two_pair(self):
        hand = [PokerCard('S', 11), PokerCard('D', 5), PokerCard('C', 8), PokerCard('D', 8), PokerCard('S', 9)]
        session = Poker(Game(uuid4()))
        self.assertEqual(session.check_two_pairs(hand), [])

    def test_kicker_gives_right_hand(self):
        hand1 = [5, 10]
        hand2 = [5, 7]
        session = Poker(Game(uuid4()))
        self.assertEqual(session.check_two_pair_kicker(hand1, hand2), hand1)


class PokerGameTestPairAndNoPair(unittest.TestCase):
    def test_is_pair(self):
        hand = [PokerCard('S', 11), PokerCard('D', 5), PokerCard('C', 8), PokerCard('D', 8), PokerCard('S', 9)]
        session = Poker(Game(uuid4()))
        self.assertEqual(session.check_one_pairs(hand), [5, 9, 11, 8])

    def test_is_not_pair(self):
        hand = [PokerCard('S', 11), PokerCard('D', 5), PokerCard('C', 4), PokerCard('D', 8), PokerCard('S', 9)]
        session = Poker(Game(uuid4()))
        self.assertEqual(session.check_one_pairs(hand), [])

    def test_kicker_gives_right_hand(self):
        hand1 = [6, 7, 8, 10]
        hand2 = [5, 6, 7, 8]
        session = Poker(Game(uuid4()))
        self.assertEqual(session.check_three_of_a_kind_kicker(hand1, hand2), hand1)

    def test_gives_correct_high_card_no_pair(self):
        hand = [PokerCard('S', 11), PokerCard('D', 5), PokerCard('C', 8), PokerCard('D', 14), PokerCard('S', 9)]
        session = Poker(Game(uuid4()))
        self.assertEqual(session.check_high_card(hand), [14])


class PokerGameGetBestHands(unittest.TestCase):
    def test_possible_hands_are_correct_length(self):
        session = Poker(Game(uuid4()))
        session.board = [PokerCard('S', 11), PokerCard('D', 5), PokerCard('C', 8),
                         PokerCard('D', 14), PokerCard('S', 9)]
        hand = [PokerCard('S', 4), PokerCard('S', 12)]

        possible_hands = session.get_possible_hands(hand)

        for hand in possible_hands:
            self.assertEqual(len(hand), 5)

    def test_possible_hands_do_not_contain_duplicates(self):
        session = Poker(Game(uuid4()))
        session.board = [PokerCard('S', 11), PokerCard('D', 5), PokerCard('C', 8),
                         PokerCard('D', 14), PokerCard('S', 9)]
        hand = [PokerCard('S', 4), PokerCard('S', 12)]

        possible_hands = session.get_possible_hands(hand)

        # should be 7 choose 5
        self.assertEqual(len(possible_hands), 21)


class PokerGameTestFIndBestHand(unittest.TestCase):
    def test_find_best_hand_replaces_with_better_hand(self):
        one_pair_hand = [PokerCard('S', 11), PokerCard('D', 5), PokerCard('C', 8),
                         PokerCard('D', 8), PokerCard('S', 9)]

        two_pair_hand = [PokerCard('S', 11), PokerCard('D', 11), PokerCard('C', 8),
                         PokerCard('D', 8), PokerCard('S', 9)]

        session = Poker(Game(uuid4()))
        best_hand = session.find_best_hand([one_pair_hand, two_pair_hand])

        self.assertEqual(best_hand[2], two_pair_hand)
        self.assertEqual(best_hand[0], 2)

        quads_hand = [PokerCard('S', 10), PokerCard('D', 10), PokerCard('C', 10), PokerCard('H', 10), PokerCard('S', 6)]
        best_hand = session.find_best_hand([one_pair_hand, two_pair_hand, quads_hand])
        self.assertEqual(best_hand[2], quads_hand)
        self.assertEqual(best_hand[0], 7)

    def test_find_best_hand_doesnt_replace_worse_hand(self):
        one_pair_hand = [PokerCard('S', 11), PokerCard('D', 5), PokerCard('C', 8),
                         PokerCard('D', 8), PokerCard('S', 9)]

        two_pair_hand = [PokerCard('S', 11), PokerCard('D', 11), PokerCard('C', 8),
                         PokerCard('D', 8), PokerCard('S', 9)]

        session = Poker(Game(uuid4()))
        best_hand = session.find_best_hand([two_pair_hand, one_pair_hand])
        self.assertEqual(best_hand[2], two_pair_hand)
        self.assertEqual(best_hand[0], 2)

    def test_find_best_hand_updates_if_better_kicker(self):
        """
        high_one_pair_hand = [PokerCard('S', 11), PokerCard('D', 5), PokerCard('C', 14),
                              PokerCard('D', 14), PokerCard('S', 9)]
        low_one_pair_hand = [PokerCard('S', 11), PokerCard('D', 5), PokerCard('C', 3),
                             PokerCard('D', 3), PokerCard('S', 9)]

        session = Poker(Game(uuid4()))
        best_hand = session.find_best_hand([low_one_pair_hand, high_one_pair_hand])
        self.assertEqual(best_hand[2], high_one_pair_hand)
        self.assertEqual(best_hand[0], 1)

        lower_straight = [PokerCard('S', 7), PokerCard('S', 11), PokerCard('S', 10),
                          PokerCard('D', 8), PokerCard('S', 9)]

        higher_straight = [PokerCard('S', 12), PokerCard('S', 11), PokerCard('S', 10),
                           PokerCard('D', 8), PokerCard('S', 9)]

        best_hand = session.find_best_hand([lower_straight, higher_straight])
        self.assertEqual(best_hand[2], higher_straight)
        self.assertEqual(best_hand[0], 4)
        """

    def test_find_best_hand_doesnt_update_if_worse_kicker(self):
        lower_straight = [PokerCard('S', 7), PokerCard('S', 11), PokerCard('S', 10),
                          PokerCard('D', 8), PokerCard('S', 9)]

        higher_straight = [PokerCard('S', 12), PokerCard('S', 11), PokerCard('S', 10),
                           PokerCard('D', 8), PokerCard('S', 9)]

        session = Poker(Game(uuid4()))
        best_hand = session.find_best_hand([higher_straight, lower_straight])
        self.assertEqual(best_hand[2], higher_straight)
        self.assertEqual(best_hand[0], 4)

class PokerGameEvaluateWinner(unittest.TestCase):
    def test_update_winner_status_resets_stakes(self):
        session = Poker(Game(uuid4()))
        user = CustomUser()
        user.username = "andrew"
        session.add_player(user)
        session.players_info["andrew"] = dict()
        session.players_info["andrew"]["stake"] = 10.0
        session.pot = 0.0
        session.update_winner_status()
        self.assertEqual(session.pot, 10.0)
        self.assertEqual(session.players_info["andrew"]["stake"], 0.0)

    def test_reset_stakes_increases_pot_and_sets_stakes_to_zero(self):
        session = Poker(Game(uuid4()))
        user = CustomUser()
        user.username = "andrew"
        session.add_player(user)
        session.players_info["andrew"] = dict()
        session.players_info["andrew"]["stake"] = 10.0
        session.pot = 0.0
        session.reset_stakes()
        self.assertEqual(session.pot, 10.0)
        self.assertEqual(session.players_info["andrew"]["stake"], 0.0)
        self.assertEqual(session.price_to_call, 0.0)

    def update_board_deals_flop_when_no_cards_are_out(self):
        session = Poker(Game(uuid4()))
        session.deck.build()
        self.board = []
        session.update_board()
        self.assertEqual(len(self.board), 3)

    def update_board_deals_turn_with_3_cards_out(self):
        session = Poker(Game(uuid4()))
        session.deck.build()
        self.board = [PokerCard('S', 7), PokerCard('S', 11), PokerCard('S', 10)]
        session.update_board()
        self.assertEqual(len(self.board), 4)

    def update_board_deals_river_with_4_cards_out(self):
        session = Poker(Game(uuid4()))
        session.deck.build()
        self.board = [PokerCard('S', 7), PokerCard('S', 11), PokerCard('S', 10), PokerCard('S', 4)]
        session.update_board()
        self.assertEqual(len(self.board), 5)

class PokerGameTestPlayerAction(unittest.TestCase):
    def test_end_round_updates_current_turn(self):
        session = Poker(Game(uuid4()))
        session.players = ["andy", "drew", "mike"]
        session.deal_cards()
        session.dealer_index = 0
        session.end_round()
        self.assertEqual(session.current_turn, 1)
        self.assertEqual(session.last_raiser, 1)

    def test_find_last_player_gives_last_player(self):
        session = Poker(Game(uuid4()))
        session.players = ["andy", "drew", "mike"]
        session.deal_cards()
        session.players_info["andy"]["folded"] = True
        session.players_info["drew"]["folded"] = True
        self.assertEqual(session.find_last_player(), session.players[2])

    def test_player_action_player_turn_not_valid(self):
        session = Poker(Game(uuid4()))
        user = CustomUser()
        user.username = "andy"
        session.players = ["andy", "drew", "mike"]

        session.deal_cards()
        session.current_turn = 1
        bet_request = {"action": "bet", "amount": 20.0, "player": user}
        session.player_action(bet_request)
        self.assertEqual(session.players_info["andy"]["stake"], 0.0)

    def test_player_action_player_bet_not_valid(self):
        session = Poker(Game(uuid4()))
        user = CustomUser()
        user.username = "andy"
        session.players = ["andy", "drew", "mike"]
        session.deal_cards()
        session.current_turn = 1
        bet_request = {"action": "bet", "amount": 20.0, "player": user}
        session.price_to_call = 21.0
        session.player_action(bet_request)
        self.assertEqual(session.players_info["andy"]["stake"], 0.0)

    def test_player_action_updates_turn(self):
        session = Poker(Game(uuid4()))
        user = CustomUser()
        user.username = "mike"
        session.players = ["andy", "drew", "mike"]
        session.deal_cards()
        session.current_turn = 2
        bet_request = {"action": "bet", "amount": 20.0, "player": user}

        session.player_action(bet_request)
        self.assertEqual(session.current_turn, 0)

        session.current_turn = 2
        check_request = {"action": "check", "player": user}
        session.player_action(check_request)
        self.assertEqual(session.current_turn, 0)

        session.current_turn = 2
        fold_request = {"action": "fold", "player": user}
        session.player_action(fold_request)
        self.assertEqual(session.current_turn, 0)

    def test_call_updates_stakes(self):
        session = Poker(Game(uuid4()))
        user = CustomUser()
        user.username = "mike"
        session.players = ["andy", "drew", "mike"]
        session.deal_cards()
        session.current_turn = 2
        session.price_to_call = 10.0

        check_request = {"action": "check", "player": user}
        session.player_action(check_request)
        self.assertEqual(session.players_info['mike']['stake'], 10.0)

    def test_bet_updates_stakes(self):
        session = Poker(Game(uuid4()))
        user = CustomUser()
        user.username = "mike"
        session.players = ["andy", "drew", "mike"]
        session.deal_cards()
        session.current_turn = 2
        bet_request = {"action": "bet", "amount": 20.0, "player": user}

        session.player_action(bet_request)
        self.assertEqual(session.players_info['mike']['stake'], 20.0)
        self.assertEqual(session.price_to_call, 20.0)
        self.assertEqual(session.last_raiser, 2)

    def test_fold_reduces_player_count(self):
        session = Poker(Game(uuid4()))
        user = CustomUser()
        user.username = "mike"
        session.players = ["andy", "drew", "mike"]
        session.deal_cards()
        session.current_turn = 2
        fold_request = {"action": "fold", "player": user}
        session.player_action(fold_request)

        self.assertTrue(session.players_info["mike"]["folded"])
        self.assertEqual(session.players_in_hand, 2)

    def test_get_next_turn_next_turn_not_folded(self):
        session = Poker(Game(uuid4()))
        user = CustomUser()
        user.username = "mike"
        session.players = ["andy", "drew", "mike"]
        session.deal_cards()
        session.current_turn = 2

        session.get_next_turn()
        self.assertEqual(session.current_turn, 0)

    def test_get_next_turn_next_turn_folded(self):
        session = Poker(Game(uuid4()))
        user = CustomUser()
        user.username = "mike"
        session.players = ["andy", "drew", "mike"]
        session.deal_cards()
        session.current_turn = 2
        session.players_info["andy"]["folded"] = True

        session.get_next_turn()
        self.assertEqual(session.current_turn, 1)

