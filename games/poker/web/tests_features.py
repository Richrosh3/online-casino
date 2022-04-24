from uuid import uuid4
from django.test import TestCase
import unittest
from games.base import Game
from games.poker.game.poker import Poker
from accounts.models import CustomUser
from games.poker.game.util import PokerCard


class PokerGamePlayerAction(unittest.TestCase):
    def test_ends_round_after_all_players_finish_action(self):
        session = Poker(Game(uuid4()))
        user = CustomUser()
        user.username = "mike"
        session.players = ["andy", "drew", "mike"]
        session.deal_cards()
        # here session current turn is 2
        check_request = {"action": "check", "player": user}
        session.player_action(check_request)
        self.assertEqual(len(session.board), 0)

        user.username = "andy"
        session.player_action(check_request)
        self.assertEqual(len(session.board), 0)

        user.username = "drew"
        session.player_action(check_request)
        self.assertEqual(len(session.board), 3)
        self.assertEqual(session.current_turn, 2)

    def test_labels_winner_after_everyone_folds(self):
        session = Poker(Game(uuid4()))
        user = CustomUser()
        user.username = "mike"
        session.players = ["andy", "drew", "mike"]
        session.deal_cards()
        # here session current turn is 2
        check_request = {"action": "check", "player": user}
        session.player_action(check_request)
        self.assertEqual(len(session.board), 0)
        self.assertEqual(session.winner, "")

        user.username = "andy"
        fold_request = {"action": "fold", "player": user}
        self.assertEqual(session.winner, "")

        session.player_action(fold_request)
        self.assertEqual(len(session.board), 0)

        user.username = "drew"
        session.player_action(fold_request)
        self.assertEqual(len(session.board), 0)
        self.assertEqual(session.players_in_hand, 1)
        self.assertEqual(session.winner, "mike")

    def test_player_action_goes_to_last_raiser(self):
        session = Poker(Game(uuid4()))
        user = CustomUser()
        user.username = "mike"
        session.players = ["andy", "drew", "mike"]
        session.deal_cards()

        # here session current turn is 2
        check_request = {"action": "check", "player": user}
        session.player_action(check_request)
        self.assertEqual(len(session.board), 0)
        self.assertEqual(session.current_turn, 0)

        user.username = "andy"
        bet_request = {"action": "bet", "player": user, "amount": 20.0}
        session.player_action(bet_request)
        self.assertEqual(len(session.board), 0)
        self.assertEqual(session.current_turn, 1)

        user.username = "drew"
        check_request = {"action": "check", "player": user}
        session.player_action(check_request)
        self.assertEqual(len(session.board), 0)
        self.assertEqual(session.current_turn, 2)

        user.username = "mike"
        check_request = {"action": "check", "player": user}
        session.player_action(check_request)
        self.assertEqual(len(session.board), 3)
        self.assertEqual(session.current_turn, 2)
        self.assertEqual(session.pot, 60.0)



