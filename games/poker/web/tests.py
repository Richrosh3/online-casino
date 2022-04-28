from decimal import Decimal
from uuid import uuid4

from django.test import TestCase

from accounts.models import CustomUser
from games.poker.game.poker import Poker, PokerHand
from games.poker.game.util import PokerCard


class TestPokerGameDeal(TestCase):
    def setUp(self) -> None:
        self.session = Poker(uuid4())
        self.user = CustomUser.objects.create_user(username="andrew")

    def test_add_player_adds_player(self):
        self.session.add_player(self.user)
        self.assertEqual(self.session.players, {self.user})

    def test_add_player_doesnt_add_duplicates(self):
        self.session.add_player(self.user)
        self.session.add_player(self.user)
        self.assertEqual(self.session.players, {self.user})
        self.assertEqual(len(self.session.players), 1)

    def test_deal_cards_deals_to_all_players(self):
        user2 = CustomUser.objects.create_user(username="andrew2")
        self.session.add_player(self.user)
        self.session.add_player(user2)
        self.session.start_round()
        self.assertEqual(len(self.session.round.hands[self.user].hand), 2)
        self.assertEqual(len(self.session.round.hands[user2].hand), 2)
        self.assertEqual(self.session.round.hands[self.user].stake, 0.0)
        self.assertEqual(self.session.round.hands[self.user].folded, False)
        self.assertEqual(self.session.round.hands[user2].stake, 0.0)
        self.assertEqual(self.session.round.hands[user2].folded, False)


class TestPokerHandTypes(TestCase):
    def setUp(self) -> None:
        self.session = Poker(uuid4())
        self.user = CustomUser.objects.create_user(username="andrew")
        self.board = []

    def test_is_straight_flush(self):
        hand = PokerHand(self.user, [PokerCard('S', 10), PokerCard('S', 9), PokerCard('S', 8), PokerCard('S', 7),
                                     PokerCard('S', 6)], self.board)
        hand_type, _ = hand.value()
        self.assertEqual(hand_type, "Straight Flush")

    def test_is_not_straight_flush(self):
        hand = PokerHand(self.user, [PokerCard('S', 10), PokerCard('S', 5), PokerCard('S', 8), PokerCard('S', 7),
                                     PokerCard('S', 6)], self.board)
        hand_type, _ = hand.value()
        self.assertNotEqual(hand_type, "Straight Flush")

    def test_is_quads(self):
        hand = PokerHand(self.user, [PokerCard('S', 10), PokerCard('D', 10), PokerCard('C', 10), PokerCard('H', 10),
                                     PokerCard('S', 6)], self.board)
        hand_type, _ = hand.value()
        self.assertEqual(hand_type, "Four of a Kind")

    def test_is_not_quads(self):
        hand = PokerHand(self.user, [PokerCard('H', 6), PokerCard('D', 10), PokerCard('C', 10), PokerCard('H', 10),
                                     PokerCard('S', 6)], self.board)
        hand_type, _ = hand.value()
        self.assertNotEqual(hand_type, "Four of a Kind")

    def test_is_full_house(self):
        hand = PokerHand(self.user, [PokerCard('S', 10), PokerCard('D', 10), PokerCard('C', 10), PokerCard('H', 6),
                                     PokerCard('S', 6)], self.board)
        hand_type, _ = hand.value()
        self.assertEqual(hand_type, "Full House")

    def test_is_not_full_house(self):
        hand = PokerHand(self.user, [PokerCard('S', 10), PokerCard('D', 10), PokerCard('C', 5), PokerCard('H', 6),
                                     PokerCard('S', 6)], self.board)
        hand_type, _ = hand.value()
        self.assertNotEqual(hand_type, "Full House")

    def test_is_flush(self):
        hand = PokerHand(self.user, [PokerCard('S', 11), PokerCard('S', 14), PokerCard('S', 10), PokerCard('S', 6),
                                     PokerCard('S', 5)], self.board)
        hand_type, _ = hand.value()
        self.assertEqual(hand_type, "Flush")

    def test_is_not_flush(self):
        hand = PokerHand(self.user,
                         [PokerCard('S', 11), PokerCard('D', 14), PokerCard('S', 10), PokerCard('S', 6),
                          PokerCard('S', 5)],
                         self.board)
        hand_type, _ = hand.value()
        self.assertNotEqual(hand_type, "Flush")

    def test_is_straight(self):
        hand = PokerHand(self.user, [PokerCard('S', 11), PokerCard('S', 12), PokerCard('S', 10), PokerCard('D', 8),
                                     PokerCard('S', 9)], self.board)
        hand_type, _ = hand.value()
        self.assertEqual(hand_type, "Straight")

    def test_is_not_straight(self):
        hand = PokerHand(self.user, [PokerCard('S', 5), PokerCard('S', 12), PokerCard('S', 10), PokerCard('D', 8),
                                     PokerCard('S', 9)], self.board)
        hand_type, _ = hand.value()
        self.assertNotEqual(hand_type, "Straight")

    def test_is_trips(self):
        hand = PokerHand(self.user, [PokerCard('S', 11), PokerCard('D', 11), PokerCard('C', 11), PokerCard('D', 8),
                                     PokerCard('S', 9)], self.board)
        hand_type, _ = hand.value()
        self.assertEqual(hand_type, "Three of a Kind")

    def test_is_not_trips(self):
        hand = PokerHand(self.user, [PokerCard('S', 12), PokerCard('D', 11), PokerCard('C', 11), PokerCard('D', 8),
                                     PokerCard('S', 9)], self.board)
        hand_type, _ = hand.value()
        self.assertNotEqual(hand_type, "Three of a Kind")

    def test_is_two_pair(self):
        hand = PokerHand(self.user, [PokerCard('S', 11), PokerCard('D', 11), PokerCard('C', 8), PokerCard('D', 8),
                                     PokerCard('S', 9)], self.board)
        hand_type, _ = hand.value()
        self.assertEqual(hand_type, "Two Pair")

    def test_is_not_two_pair(self):
        hand = PokerHand(self.user, [PokerCard('S', 11), PokerCard('D', 5), PokerCard('C', 8), PokerCard('D', 8),
                                     PokerCard('S', 9)], self.board)
        hand_type, _ = hand.value()
        self.assertNotEqual(hand_type, "Two Pair")

    def test_is_pair(self):
        hand = PokerHand(self.user, [PokerCard('S', 11), PokerCard('D', 5), PokerCard('C', 8), PokerCard('D', 8),
                                     PokerCard('S', 9)], self.board)
        hand_type, _ = hand.value()
        self.assertEqual(hand_type, "One Pair")

    def test_is_not_pair(self):
        hand = PokerHand(self.user, [PokerCard('S', 11), PokerCard('D', 5), PokerCard('C', 4), PokerCard('D', 8),
                                     PokerCard('S', 9)], self.board)
        hand_type, _ = hand.value()
        self.assertNotEqual(hand_type, "One Pair")


class PokerGameTestFindBestHand(TestCase):
    def setUp(self) -> None:
        self.session = Poker(uuid4())
        self.user = CustomUser.objects.create_user(username="andrew")
        self.board = []

    def test_find_best_hand_replaces_with_better_hand(self):
        one_pair_hand = PokerHand(self.user, [PokerCard('S', 11), PokerCard('D', 5), PokerCard('C', 8),
                                              PokerCard('D', 8), PokerCard('S', 9)], self.board)

        two_pair_hand = PokerHand(self.user, [PokerCard('S', 11), PokerCard('D', 11), PokerCard('C', 8),
                                              PokerCard('D', 8), PokerCard('S', 9)], self.board)

        self.assertTrue(one_pair_hand.value()[1] < two_pair_hand.value()[1])

        quads_hand = PokerHand(self.user,
                               [PokerCard('S', 10), PokerCard('D', 10), PokerCard('C', 10), PokerCard('H', 10),
                                PokerCard('S', 6)], self.board)
        self.assertTrue(one_pair_hand.value()[1] < two_pair_hand.value()[1] < quads_hand.value()[1])

    def test_find_best_hand_updates_if_better_kicker(self):
        high_one_pair_hand = PokerHand(self.user, [PokerCard('S', 11), PokerCard('D', 5), PokerCard('C', 14),
                                                   PokerCard('D', 14), PokerCard('S', 9)], self.board)
        low_one_pair_hand = PokerHand(self.user, [PokerCard('S', 11), PokerCard('D', 5), PokerCard('C', 3),
                                                  PokerCard('D', 3), PokerCard('S', 9)], self.board)
        self.assertTrue(low_one_pair_hand.value()[1] < high_one_pair_hand.value()[1])

        lower_straight = PokerHand(self.user, [PokerCard('S', 7), PokerCard('S', 11), PokerCard('S', 10),
                                               PokerCard('D', 8), PokerCard('S', 9)], self.board)

        higher_straight = PokerHand(self.user, [PokerCard('S', 12), PokerCard('S', 11), PokerCard('S', 10),
                                                PokerCard('D', 8), PokerCard('S', 9)], self.board)

        self.assertTrue(lower_straight.value()[1] < higher_straight.value()[1])


class PokerGameEvaluateWinner(TestCase):
    def setUp(self) -> None:
        self.session = Poker(uuid4())
        self.user = CustomUser.objects.create_user(username="andrew")
        self.session.players = {self.user}
        self.session.start_round()
        self.round = self.session.round

    def test_reset_stakes_increases_pot_and_sets_stakes_to_zero(self):
        self.round.hands[self.user].stake = 10.0
        self.round.pot = 0.0
        self.round.reset_stakes()
        self.assertEqual(self.round.pot, 10.0)
        self.assertEqual(self.round.hands[self.user].stake, 0.0)
        self.assertEqual(self.round.price_to_call, 0.0)

    def test_update_board_deals_flop_when_no_cards_are_out(self):
        self.round.update_board()
        self.assertEqual(len(self.round.board), 3)

    def test_update_board_deals_turn_with_3_cards_out(self):
        self.round.board = [PokerCard('S', 7), PokerCard('S', 11), PokerCard('S', 10)]
        self.round.update_board()
        self.assertEqual(len(self.round.board), 4)

    def test_update_board_deals_river_with_4_cards_out(self):
        self.round.board = [PokerCard('S', 7), PokerCard('S', 11), PokerCard('S', 10), PokerCard('S', 4)]
        self.round.update_board()
        self.assertEqual(len(self.round.board), 5)


class TestPokerGamePlayerAction(TestCase):
    def setUp(self) -> None:
        self.session = Poker(uuid4())
        self.andy = CustomUser.objects.create_user(username="andy", current_balance=Decimal(100))
        self.drew = CustomUser.objects.create_user(username="drew", current_balance=Decimal(100))
        self.mike = CustomUser.objects.create_user(username="mike", current_balance=Decimal(100))
        self.session.players = {self.andy, self.drew, self.mike}
        self.session.start_round()
        self.round = self.session.round

    def test_player_action_player_turn_not_valid(self):
        self.round.players_in_hand.rotate(-1)
        self.round.player_action(self.andy, "bet", 20.0)
        self.assertEqual(self.round.hands[self.andy].stake, 0.0)

    def test_player_action_player_bet_not_valid(self):
        self.round.price_to_call = 21.0
        self.round.player_action(self.andy, "bet", 20.0)
        self.assertEqual(self.round.hands[self.andy].stake, 0.0)

    def test_player_action_updates_turn(self):
        self.round.players_in_hand.rotate(-2)
        self.round.player_action(self.mike, "bet", 20.0)

        self.assertEqual(self.round.players_in_hand[0], self.andy)

        self.round.players_in_hand.rotate(-2)
        self.round.player_action(self.mike, "check", 20.0)

        self.assertEqual(self.round.players_in_hand[0], self.andy)

        self.round.players_in_hand.rotate(-2)
        self.round.player_action(self.mike, "fold", 20.0)

        self.assertEqual(self.round.players_in_hand[0], self.andy)

    def test_call_updates_stakes(self):
        self.round.players_in_hand.rotate(-1)
        self.round.price_to_call = 10.0

        self.round.player_action(self.drew, "check", 0)
        self.assertEqual(self.round.hands[self.drew].stake, 10.0)

    def test_bet_updates_stakes(self):
        self.round.players_in_hand.rotate(-1)

        self.round.player_action(self.drew, "bet", 20.0)
        self.assertEqual(self.round.hands[self.drew].stake, 20.0)
        self.assertEqual(self.round.price_to_call, 20.0)
        self.assertEqual(self.round.last_raiser, self.drew)

    def test_fold_reduces_player_count(self):
        self.round.players_in_hand.rotate(-1)
        self.round.player_action(self.drew, "fold", 0.0)

        self.assertTrue(self.round.hands[self.drew].folded)
        self.assertEqual(len(self.round.players_in_hand), 2)

    def test_get_next_turn_next_turn_not_folded(self):
        self.round.players_in_hand.rotate(-2)

        self.round.change_turn()
        self.assertEqual(self.round.players_in_hand[0], self.andy)

    def test_get_next_turn_next_turn_folded(self):
        self.round.player_action(self.andy, "fold", 0.0)
        self.round.players_in_hand.rotate(-1)

        self.round.change_turn()
        self.assertEqual(self.round.players_in_hand[0], self.drew)
