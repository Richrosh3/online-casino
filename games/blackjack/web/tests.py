from decimal import Decimal
from uuid import uuid4

from django.contrib import auth
from django.test import TestCase

from accounts.models import CustomUser
from games.blackjack.game.blackjack import BlackjackRound
from games.blackjack.game.utils import Pack, BlackjackCard
from games.blackjack.web.views import BLACKJACK_MANAGER


class TestBlackjackManager(TestCase):
    """
    Testing the blackjack session manager
    """

    def setUp(self) -> None:
        CustomUser.objects.create_user(username='user', password='pass')
        self.client.login(username='user', password='pass')
        self.user = auth.get_user(self.client)

    def tearDown(self) -> None:
        BLACKJACK_MANAGER.sessions = {}

    def test_create_session_creates_new_session(self):
        self.assertEqual(0, len(BLACKJACK_MANAGER.sessions))
        BLACKJACK_MANAGER.create()
        self.assertEqual(1, len(BLACKJACK_MANAGER.sessions))

    def test_register_user_adds_player_to_game(self):
        session_id = BLACKJACK_MANAGER.create()
        BLACKJACK_MANAGER.register_user(session_id, self.user)
        self.assertTrue(self.user in BLACKJACK_MANAGER.sessions[session_id].players)

    def test_remove_user_removes_a_user_from_the_game(self):
        session_id = BLACKJACK_MANAGER.create()
        BLACKJACK_MANAGER.register_user(session_id, self.user)
        self.assertTrue(self.user in BLACKJACK_MANAGER.sessions[session_id].players)
        BLACKJACK_MANAGER.remove_user(session_id, self.user)
        self.assertFalse(self.user in BLACKJACK_MANAGER.sessions[session_id].players)

    def test_session_does_not_exist(self):
        self.assertFalse(BLACKJACK_MANAGER.session_exists(uuid4()))

    def test_session_exists(self):
        session_id = BLACKJACK_MANAGER.create()
        self.assertTrue(BLACKJACK_MANAGER.session_exists(session_id))

    def test_list_sessions_with_no_sessions(self):
        self.assertEqual({}, BLACKJACK_MANAGER.list_sessions())

    def test_list_sessions_with_active_sessions(self):
        BLACKJACK_MANAGER.create()
        BLACKJACK_MANAGER.create()
        self.assertEqual(2, len(BLACKJACK_MANAGER.list_sessions()))

    def test_get_session_that_doesnt_exist(self):
        self.assertIsNone(BLACKJACK_MANAGER.get(uuid4()))

    def test_get_session_that_exists(self):
        session_id = BLACKJACK_MANAGER.create()
        self.assertIsNotNone(BLACKJACK_MANAGER.get(session_id))

    def test_delete_nonexistent_session(self):
        self.assertIsNone(BLACKJACK_MANAGER.delete(uuid4()))

    def test_delete_existent_session(self):
        session_id = BLACKJACK_MANAGER.create()
        self.assertEqual(1, len(BLACKJACK_MANAGER.sessions))
        self.assertIsNotNone(BLACKJACK_MANAGER.delete(session_id))
        self.assertEqual(0, len(BLACKJACK_MANAGER.sessions))


class TestBlackJackGame(TestCase):
    """
    Testing the Blackjack class
    """

    def setUp(self) -> None:
        CustomUser.objects.create_user(username='user', password='pass', current_balance=Decimal(300))
        self.client.login(username='user', password='pass')
        self.user = auth.get_user(self.client)
        self.session_id = BLACKJACK_MANAGER.create()
        BLACKJACK_MANAGER.register_user(self.session_id, self.user)
        self.game = BLACKJACK_MANAGER.get(self.session_id)

    def tearDown(self) -> None:
        BLACKJACK_MANAGER.sessions = {}

    def test_not_all_ready(self):
        self.assertFalse(self.game.all_ready())

    def test_all_ready(self):
        for player in self.game.players_ready:
            self.game.players_ready[player] = True
        self.assertTrue(self.game.all_ready())

    def test_recording_bet(self):
        self.assertEqual(0, self.game.bets[self.user])
        self.game.record_bet(self.user, 100)
        self.assertEqual(100, self.game.bets[self.user])

    def test_ready_up_to_ready(self):
        extra_user = CustomUser.objects.create_user(username='extra_user', password='pass')
        BLACKJACK_MANAGER.register_user(self.session_id, extra_user)
        self.game.ready_up(self.user, True)
        self.assertTrue(self.game.players_ready[self.user])

    def test_ready_up_to_unready(self):
        extra_user = CustomUser.objects.create_user(username='extra_user', password='pass')
        BLACKJACK_MANAGER.register_user(self.session_id, extra_user)
        self.game.ready_up(self.user, False)
        self.assertFalse(self.game.players_ready[self.user])

    def test_get_stage_is_betting(self):
        self.game.round = None
        self.assertEqual('betting', self.game.get_stage())

    def test_get_stage_is_dealing(self):
        self.game.round = BlackjackRound(Pack(card_class=BlackjackCard), self.game)
        self.assertEqual('dealing', self.game.get_stage())

    def test_get_stage_is_ending(self):
        self.game.round = BlackjackRound(Pack(card_class=BlackjackCard), self.game)
        self.game.round.round_over = True
        self.assertEqual('ending', self.game.get_stage())

    def test_reset_round(self):
        self.game.start_round()
        self.assertIsNotNone(self.game.round)
        self.game.reset()
        self.assertIsNone(self.game.round)

    def test_start_round(self):
        self.assertIsNone(self.game.round)
        self.game.start_round()
        self.assertIsNotNone(self.game.round)

    def test_record_bets(self):
        self.game.bets[self.user] = 100
        self.game.record_bets()
        self.user.refresh_from_db()
        self.assertEqual(Decimal(200), self.user.current_balance)

    def test_remove_player_removes_player(self):
        self.game.remove_player(self.user)
        self.assertEqual(0, len(self.game.players))
        self.assertEqual(0, len(self.game.players_ready))
        self.assertEqual(0, len(self.game.bets))

    def test_check_update_game_stage_betting(self):
        self.game.players_ready[self.user] = True
        self.game.check_update_game_stage()
        self.assertFalse(self.game.players_ready[self.user])

    def test_check_update_game_stage_ending(self):
        self.game.players_ready[self.user] = True
        self.game.round = BlackjackRound(Pack(card_class=BlackjackCard), self.game)
        self.game.round.round_over = True
        self.game.check_update_game_stage()
        self.assertIsNone(self.game.round)

    def test_add_player_during_betting(self):
        extra_user = CustomUser.objects.create_user(username='extra_user', password='pass')
        self.game.add_player(extra_user)
        self.assertTrue(extra_user in self.game.players)

    def test_add_player_during_dealing(self):
        extra_user = CustomUser.objects.create_user(username='extra_user', password='pass')
        self.game.round = BlackjackRound(Pack(card_class=BlackjackCard), self.game)
        self.game.add_player(extra_user)
        self.assertFalse(extra_user in self.game.players)
        self.assertTrue(extra_user in self.game.waiting_room)

    def test_add_player_during_ending(self):
        extra_user = CustomUser.objects.create_user(username='extra_user', password='pass')
        self.game.round = BlackjackRound(Pack(card_class=BlackjackCard), self.game)
        self.game.round.round_over = True
        self.game.add_player(extra_user)
        self.assertFalse(extra_user in self.game.players)
        self.assertTrue(extra_user in self.game.waiting_room)

    def test_dict_representation_during_betting(self):
        self.assertEqual({'players': [{'bet': '0', 'player': 'user', 'ready': False}], 'stage': 'betting'},
                         self.game.dict_representation())

    def test_dict_representation_during_dealing(self):
        self.game.start_round()
        self.assertEqual('dealing', self.game.dict_representation()['stage'])

    def test_dict_representation_during_ending(self):
        self.game.start_round()
        self.game.round.play_dealer()
        self.assertEqual('ending', self.game.dict_representation()['stage'])


class TestBlackjackRound(TestCase):
    """
    Testing the BlackjackRound class
    """

    def setUp(self) -> None:
        CustomUser.objects.create_user(username='user', password='pass', current_balance=Decimal(300))
        self.client.login(username='user', password='pass')
        self.user = auth.get_user(self.client)
        self.session_id = BLACKJACK_MANAGER.create()
        BLACKJACK_MANAGER.register_user(self.session_id, self.user)
        extra_user = CustomUser.objects.create_user(username='extra_user', password='pass')
        BLACKJACK_MANAGER.register_user(self.session_id, extra_user)
        self.game = BLACKJACK_MANAGER.get(self.session_id)
        self.game.start_round()
        self.round = self.game.round

    def tearDown(self) -> None:
        BLACKJACK_MANAGER.sessions = {}

    def test_inti_initializes_hand_with_two_cards(self):
        for player in self.round.hands:
            self.assertEqual(2, len(self.round.hands[player].hand))

    def test_check_for_blackjack_readys_player_who_has_blackjack(self):
        self.round.hands[self.user].hand = [BlackjackCard('S', 'A'), BlackjackCard('S', 'K')]
        self.round.check_for_blackjack()
        self.assertTrue(self.game.players_ready[self.user])

    def test_check_for_blackjack_doesnt_ready_player_who_doesnt_have_blackjack(self):
        self.round.hands[self.user].hand = [BlackjackCard('S', 6), BlackjackCard('S', 'K')]
        self.round.check_for_blackjack()
        self.assertFalse(self.game.players_ready[self.user])

    def test_check_dealers_turn_when_all_ready(self):
        for player in self.game.players_ready.keys():
            self.game.players_ready[player] = True

        self.round.check_dealers_turn()
        self.assertTrue(self.round.round_over)

    def test_check_dealers_turn_when_not_all_ready(self):
        self.game.players_ready[self.user] = True

        self.round.check_dealers_turn()
        self.assertFalse(self.round.round_over)

    def test_update_game_hit_under_21(self):
        self.round.hands[self.user].hand = []
        self.round.update_game(self.user, 'hit')
        self.assertEqual(1, len(self.round.hands[self.user].hand))
        self.assertFalse(self.game.players_ready[self.user])

    def test_update_game_hit_goes_over_21(self):
        self.round.hands[self.user].hand = [BlackjackCard('S', 'K'), BlackjackCard('S', 'K'), BlackjackCard('H', 'K')]
        self.round.update_game(self.user, 'hit')
        self.assertEqual(4, len(self.round.hands[self.user].hand))
        self.assertTrue(self.game.players_ready[self.user])

    def test_update_game_stay_readys_player(self):
        self.round.update_game(self.user, 'stay')
        self.assertTrue(self.game.players_ready[self.user])

    def test_remove_player(self):
        self.round.remove_player(self.user)
        self.assertFalse(self.user in self.round.hands.keys())

    def test_play_dealer(self):
        self.round.play_dealer()
        self.assertTrue(self.round.round_over)

    def test_payout_for_blackjack(self):
        self.round.hands[self.user].hand = [BlackjackCard('S', 'K'), BlackjackCard('S', 'A')]
        self.game.bets[self.user] = 100
        self.round.dealer.hand = [BlackjackCard('C', 8), BlackjackCard('S', 'K')]
        self.round.hands[self.user].calculate_outcome(self.round.dealer)
        self.round.payout_hand(self.user, self.round.hands[self.user])
        self.user.refresh_from_db()
        self.assertEqual(Decimal(550), self.user.current_balance)

    def test_payout_for_win(self):
        self.round.hands[self.user].hand = [BlackjackCard('C', 'K'), BlackjackCard('S', 'K'), BlackjackCard('S', 'A')]
        self.game.bets[self.user] = 100
        self.round.dealer.hand = [BlackjackCard('C', 8), BlackjackCard('S', 'K')]
        self.round.hands[self.user].calculate_outcome(self.round.dealer)
        self.round.payout_hand(self.user, self.round.hands[self.user])
        self.user.refresh_from_db()
        self.assertEqual(Decimal(500), self.user.current_balance)

    def test_payout_for_push(self):
        self.round.hands[self.user].hand = [BlackjackCard('C', 8), BlackjackCard('S', 'K')]
        self.game.bets[self.user] = 100
        self.round.dealer.hand = [BlackjackCard('C', 8), BlackjackCard('S', 'K')]
        self.round.hands[self.user].calculate_outcome(self.round.dealer)
        self.round.payout_hand(self.user, self.round.hands[self.user])
        self.user.refresh_from_db()
        self.assertEqual(Decimal(400), self.user.current_balance)

    def test_payout_for_loss(self):
        self.round.hands[self.user].hand = [BlackjackCard('C', 8), BlackjackCard('S', 'K')]
        self.game.bets[self.user] = 100
        self.round.dealer.hand = [BlackjackCard('C', 10), BlackjackCard('S', 'K')]
        self.round.hands[self.user].calculate_outcome(self.round.dealer)
        self.round.payout_hand(self.user, self.round.hands[self.user])
        self.user.refresh_from_db()
        self.assertEqual(Decimal(300), self.user.current_balance)
