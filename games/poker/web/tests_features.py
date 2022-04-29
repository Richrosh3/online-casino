from decimal import Decimal
from uuid import uuid4

from django.test import TestCase

from accounts.models import CustomUser
from games.poker.game.poker import Poker


class TestPokerGamePlayerAction(TestCase):
    def setUp(self) -> None:
        self.session = Poker(uuid4())
        self.andy = CustomUser.objects.create_user(username="andy", current_balance=Decimal(100))
        self.drew = CustomUser.objects.create_user(username="drew", current_balance=Decimal(100))
        self.mike = CustomUser.objects.create_user(username="mike", current_balance=Decimal(100))
        self.session.players = {self.andy, self.drew, self.mike}
        self.session.start_round()
        self.round = self.session.round

    def test_ends_round_after_all_players_finish_action(self):
        self.round.player_action(self.andy, "check", 0)
        self.assertEqual(len(self.round.board), 0)

        self.round.player_action(self.drew, "check", 0)
        self.assertEqual(len(self.round.board), 0)

        self.round.player_action(self.mike, "check", 0)
        self.assertEqual(len(self.round.board), 3)

        self.assertEqual(self.round.players_in_hand[0], self.andy)

    def test_labels_winner_after_everyone_folds(self):
        self.round.player_action(self.andy, "check", 0)

        self.assertEqual(len(self.round.board), 0)
        self.assertEqual(self.round.winners, [])

        self.round.player_action(self.drew, "fold", 0)

        self.assertEqual(len(self.round.board), 0)
        self.assertEqual(self.round.winners, [])

        self.round.player_action(self.mike, "fold", 0)

        self.assertEqual(len(self.round.board), 0)
        self.assertEqual(len(self.round.players_in_hand), 1)
        self.assertEqual(self.round.winners, [self.andy])

    def test_player_action_goes_to_last_raiser(self):
        self.round.player_action(self.andy, "check", 0)

        self.assertEqual(len(self.round.board), 0)
        self.assertEqual(self.round.players_in_hand[0], self.drew)

        self.round.player_action(self.drew, "bet", 20)
        self.assertEqual(len(self.round.board), 0)
        self.assertEqual(self.round.players_in_hand[0], self.mike)

        self.round.player_action(self.mike, "check", 0)
        self.assertEqual(len(self.round.board), 0)
        self.assertEqual(self.round.players_in_hand[0], self.andy)

        self.round.player_action(self.andy, "check", 0)
        self.assertEqual(len(self.round.board), 3)
        self.assertEqual(self.round.players_in_hand[0], self.drew)
        self.assertEqual(self.round.pot, 60.0)
