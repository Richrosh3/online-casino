from uuid import uuid4

from channels.testing import WebsocketCommunicator
from django.contrib import auth
from django.test import TestCase

from OnlineCasino.asgi import application
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
        CustomUser.objects.create_user(username='user', password='pass', current_balance=300)
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
        pack = Pack(card_class=BlackjackCard)
        pack.deck = [BlackjackCard('S', 2) for _ in range(50)]
        self.game.round = BlackjackRound(pack, self.game)
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
        self.assertEqual(200, self.user.current_balance)

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
        pack = Pack(card_class=BlackjackCard)
        pack.deck = [BlackjackCard('S', 2) for _ in range(50)]
        self.game.round = BlackjackRound(pack, self.game)
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
        self.assertEqual(
            {'players': [{'bet': '0', 'player': 'user', 'ready': False}], 'stage': 'betting', 'spectating': []},
            self.game.dict_representation())

    def test_dict_representation_during_dealing(self):
        pack = Pack(card_class=BlackjackCard)
        pack.deck = [BlackjackCard('S', 2) for _ in range(50)]
        self.game.round = BlackjackRound(pack, self.game)
        self.assertEqual('dealing', self.game.dict_representation()['stage'])

    def test_dict_representation_during_ending(self):
        pack = Pack(card_class=BlackjackCard)
        pack.deck = [BlackjackCard('S', 2) for _ in range(50)]
        self.game.round = BlackjackRound(pack, self.game)
        self.game.round.round_over = True
        self.assertEqual('ending', self.game.dict_representation()['stage'])


class TestBlackjackRound(TestCase):
    """
    Testing the BlackjackRound class
    """

    def setUp(self) -> None:
        CustomUser.objects.create_user(username='user', password='pass', current_balance=300)
        self.client.login(username='user', password='pass')
        self.user = auth.get_user(self.client)
        self.session_id = BLACKJACK_MANAGER.create()
        BLACKJACK_MANAGER.register_user(self.session_id, self.user)
        extra_user = CustomUser.objects.create_user(username='extra_user', password='pass')
        BLACKJACK_MANAGER.register_user(self.session_id, extra_user)
        self.game = BLACKJACK_MANAGER.get(self.session_id)
        pack = Pack(card_class=BlackjackCard)
        pack.deck = [BlackjackCard('S', 2) for _ in range(50)]
        self.round = BlackjackRound(pack, self.game)

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
        self.assertEqual(550, self.user.current_balance)

    def test_payout_for_win(self):
        self.round.hands[self.user].hand = [BlackjackCard('C', 'K'), BlackjackCard('S', 'K'), BlackjackCard('S', 'A')]
        self.game.bets[self.user] = 100
        self.round.dealer.hand = [BlackjackCard('C', 8), BlackjackCard('S', 'K')]
        self.round.hands[self.user].calculate_outcome(self.round.dealer)
        self.round.payout_hand(self.user, self.round.hands[self.user])
        self.user.refresh_from_db()
        self.assertEqual(500, self.user.current_balance)

    def test_payout_for_push(self):
        self.round.hands[self.user].hand = [BlackjackCard('C', 8), BlackjackCard('S', 'K')]
        self.game.bets[self.user] = 100
        self.round.dealer.hand = [BlackjackCard('C', 8), BlackjackCard('S', 'K')]
        self.round.hands[self.user].calculate_outcome(self.round.dealer)
        self.round.payout_hand(self.user, self.round.hands[self.user])
        self.user.refresh_from_db()
        self.assertEqual(400, self.user.current_balance)

    def test_payout_for_loss(self):
        self.round.hands[self.user].hand = [BlackjackCard('C', 8), BlackjackCard('S', 'K')]
        self.game.bets[self.user] = 100
        self.round.dealer.hand = [BlackjackCard('C', 10), BlackjackCard('S', 'K')]
        self.round.hands[self.user].calculate_outcome(self.round.dealer)
        self.round.payout_hand(self.user, self.round.hands[self.user])
        self.user.refresh_from_db()
        self.assertEqual(300, self.user.current_balance)


# class TestBlackjackWebSocket(TestCase):
#     def setUp(self) -> None:
#         self.user = CustomUser.objects.create_user(username='user', password='pass', current_balance=1000)
#         self.user_two = CustomUser.objects.create_user(username='user_two', password='pass', current_balance=1000)
#         self.client.login(username='user', password='pass')
#         self.unique_id = BLACKJACK_MANAGER.create()
#
#     def tearDown(self) -> None:
#         BLACKJACK_MANAGER.sessions = {}
#
#     async def test_connects_to_websocket(self):
#         communicator = WebsocketCommunicator(application, "ws/blackjack/{}/".format(self.unique_id))
#         communicator.scope['user'] = self.user
#         connected, _ = await communicator.connect()
#         self.assertTrue(connected)
#         await communicator.disconnect()
#
#     async def test_connects_to_websocket_from_limbo(self):
#         BLACKJACK_MANAGER.get(self.unique_id).add_to_limbo(self.user)
#         communicator = WebsocketCommunicator(application, "ws/blackjack/{}/".format(self.unique_id))
#         communicator.scope['user'] = self.user
#         connected, _ = await communicator.connect()
#         self.assertTrue(connected)
#         await communicator.disconnect()
#
#     async def test_disconnects_to_websocket_only_user_in_session(self):
#         communicator = WebsocketCommunicator(application, "ws/blackjack/{}/".format(self.unique_id))
#         communicator.scope['user'] = self.user
#         connected, _ = await communicator.connect()
#         self.assertTrue(connected)
#         await communicator.disconnect()
#
#     async def test_disconnects_to_websocket_multiple_users_in_session(self):
#         communicator_1 = WebsocketCommunicator(application, "ws/blackjack/{}/".format(self.unique_id))
#         communicator_1.scope['user'] = self.user
#         connected, _ = await communicator_1.connect()
#         self.assertTrue(connected)
#         communicator_2 = WebsocketCommunicator(application, "ws/blackjack/{}/".format(self.unique_id))
#         communicator_2.scope['user'] = self.user_two
#         connected, _ = await communicator_2.connect()
#         self.assertTrue(connected)
#         await communicator_1.disconnect()
#         self.assertTrue(self.unique_id in BLACKJACK_MANAGER.sessions.keys())
#         await communicator_2.disconnect()
#         self.assertTrue(self.unique_id not in BLACKJACK_MANAGER.sessions.keys())
#
#     async def test_receive_load_game(self):
#         communicator = WebsocketCommunicator(application, "ws/blackjack/{}/".format(self.unique_id))
#         communicator.scope['user'] = self.user
#         await communicator.connect()
#         await communicator.send_json_to({"type": "load_game"})
#         response = await communicator.receive_json_from()
#         self.assertEqual({'type': 'load_game',
#                           'data': {'stage': 'betting', 'players': [{'player': 'user', 'bet': '0', 'ready': False}],
#                                    'spectating': []},
#                           'user': 'user'}, response)
#         await communicator.disconnect()
#
#     async def test_receive_load_game_updates_all_users_game(self):
#         communicator_1 = WebsocketCommunicator(application, "ws/blackjack/{}/".format(self.unique_id))
#         communicator_1.scope['user'] = self.user
#         await communicator_1.connect()
#         communicator_2 = WebsocketCommunicator(application, "ws/blackjack/{}/".format(self.unique_id))
#         communicator_2.scope['user'] = self.user_two
#         await communicator_2.connect()
#         await communicator_1.send_json_to({"type": "load_game"})
#         response = await communicator_2.receive_json_from()
#         self.assertEqual({'type': 'load_game',
#                           'data': {'stage': 'betting', 'players': [{'player': 'user', 'bet': '0', 'ready': False},
#                                                                    {'player': 'user_two', 'bet': '0', 'ready': False}],
#                                    'spectating': []},
#                           'user': 'user_two'}, response)
#         await communicator_1.disconnect()
#         await communicator_2.disconnect()
#
#     async def test_receive_place_bet(self):
#         communicator = WebsocketCommunicator(application, "ws/blackjack/{}/".format(self.unique_id))
#         communicator.scope['user'] = self.user
#         await communicator.connect()
#         _ = await communicator.receive_json_from()
#         BLACKJACK_MANAGER.get(self.unique_id).start_round()
#         await communicator.send_json_to({"type": "place_bet", 'data': {'bet': 10}})
#         response = await communicator.receive_json_from()
#         self.assertEqual(10, float(response['data']['players'][0]['bet']))
#         await communicator.disconnect()
#
#     async def test_receive_ready_up(self):
#         communicator = WebsocketCommunicator(application, "ws/blackjack/{}/".format(self.unique_id))
#         communicator.scope['user'] = self.user
#         await communicator.connect()
#         _ = await communicator.receive_json_from()
#         communicator_2 = WebsocketCommunicator(application, "ws/blackjack/{}/".format(self.unique_id))
#         communicator_2.scope['user'] = self.user_two
#         await communicator_2.connect()
#         _ = await communicator.receive_json_from()
#         await communicator.send_json_to({"type": "ready_up", 'data': {'ready': True, 'reset': False}})
#         response = await communicator.receive_json_from()
#         self.assertTrue(response['data']['players'][0]['ready'])
#         self.assertFalse(response['data']['players'][1]['ready'])
#         await communicator.disconnect()
#         await communicator_2.disconnect()
#
#     async def test_receive_ready_up_one_player(self):
#         communicator = WebsocketCommunicator(application, "ws/blackjack/{}/".format(self.unique_id))
#         communicator.scope['user'] = self.user
#         await communicator.connect()
#         _ = await communicator.receive_json_from()
#         await communicator.send_json_to({"type": "ready_up", 'data': {'ready': True, 'reset': False}})
#         response = await communicator.receive_json_from()
#         self.assertFalse(response['data']['players'][0]['ready'])
#         self.assertEqual('dealing', response['data']['stage'])
#         await communicator.disconnect()
#
#     async def test_receive_make_move(self):
#         communicator = WebsocketCommunicator(application, "ws/blackjack/{}/".format(self.unique_id))
#         communicator.scope['user'] = self.user
#         await communicator.connect()
#         _ = await communicator.receive_json_from()
#         BLACKJACK_MANAGER.get(self.unique_id).start_round()
#         await communicator.send_json_to({'type': 'action', 'data': {'move': 'hit'}})
#         response = await communicator.receive_json_from()
#         self.assertEqual(3, len(response['data']['hands'][0]['hand']))
#         await communicator.disconnect()
#
#     async def test_receive_player_balance(self):
#         communicator = WebsocketCommunicator(application, "ws/blackjack/{}/".format(self.unique_id))
#         communicator.scope['user'] = self.user
#         await communicator.connect()
#         _ = await communicator.receive_json_from()
#         await communicator.send_json_to({'type': 'request_user_balance'})
#         response = await communicator.receive_json_from()
#         self.assertEqual(self.user.current_balance, float(response['data']['balance']))
#         await communicator.disconnect()
