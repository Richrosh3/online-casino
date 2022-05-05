from uuid import uuid4

from channels.testing import WebsocketCommunicator
from django.contrib import auth
from django.test import TestCase

from OnlineCasino.asgi import application
from accounts.models import CustomUser
from games.roulette.web.views import ROULETTE_MANAGER


class TestRouletteManager(TestCase):
    def setUp(self) -> None:
        CustomUser.objects.create_user(username='user', password='pass')
        self.client.login(username='user', password='pass')
        self.user = auth.get_user(self.client)

    def tearDown(self) -> None:
        ROULETTE_MANAGER.sessions = {}

    def test_create_session_creates_new_session(self):
        self.assertEqual(0, len(ROULETTE_MANAGER.sessions))
        ROULETTE_MANAGER.create()
        self.assertEqual(1, len(ROULETTE_MANAGER.sessions))

    def test_register_user_adds_player_to_game(self):
        session_id = ROULETTE_MANAGER.create()
        ROULETTE_MANAGER.register_user(session_id, self.user)
        self.assertTrue(self.user in ROULETTE_MANAGER.sessions[session_id].players)

    def test_remove_user_removes_a_user_from_the_game(self):
        session_id = ROULETTE_MANAGER.create()
        ROULETTE_MANAGER.register_user(session_id, self.user)
        self.assertTrue(self.user in ROULETTE_MANAGER.sessions[session_id].players)
        ROULETTE_MANAGER.remove_user(session_id, self.user)
        self.assertFalse(self.user in ROULETTE_MANAGER.sessions[session_id].players)

    def test_session_does_not_exist(self):
        self.assertFalse(ROULETTE_MANAGER.session_exists(uuid4()))

    def test_session_exists(self):
        session_id = ROULETTE_MANAGER.create()
        self.assertTrue(ROULETTE_MANAGER.session_exists(session_id))

    def test_list_sessions_with_no_sessions(self):
        self.assertEqual({}, ROULETTE_MANAGER.list_sessions())

    def test_list_sessions_with_active_sessions(self):
        ROULETTE_MANAGER.create()
        ROULETTE_MANAGER.create()
        self.assertEqual(2, len(ROULETTE_MANAGER.list_sessions()))

    def test_get_session_that_doesnt_exist(self):
        self.assertIsNone(ROULETTE_MANAGER.get(uuid4()))

    def test_get_session_that_exists(self):
        session_id = ROULETTE_MANAGER.create()
        self.assertIsNotNone(ROULETTE_MANAGER.get(session_id))

    def test_delete_nonexistent_session(self):
        self.assertIsNone(ROULETTE_MANAGER.delete(uuid4()))

    def test_delete_existent_session(self):
        session_id = ROULETTE_MANAGER.create()
        self.assertEqual(1, len(ROULETTE_MANAGER.sessions))
        self.assertIsNotNone(ROULETTE_MANAGER.delete(session_id))
        self.assertEqual(0, len(ROULETTE_MANAGER.sessions))


class TestRouletteGame(TestCase):
    """
        Testing Roulette class
    """

    def setUp(self) -> None:
        CustomUser.objects.create_user(username='user', password='pass', current_balance=300)
        self.client.login(username='user', password='pass')
        self.user = auth.get_user(self.client)
        self.session_id = ROULETTE_MANAGER.create()
        ROULETTE_MANAGER.register_user(self.session_id, self.user)
        self.game = ROULETTE_MANAGER.get(self.session_id)

    def tearDown(self) -> None:
        ROULETTE_MANAGER.sessions = {}

    def test_not_all_ready(self):
        self.assertFalse(self.game.all_ready())

    def test_all_ready(self):
        for player in self.game.bet_amount:
            self.game.bet_amount[player] = 10
            self.game.bet_type[player] = {'type': 'odd'}
        self.assertTrue(self.game.all_ready())

    def test_recording_bet(self):
        self.game.record_bet(self.user, 100, {'type': 'odd'})
        self.assertTrue(self.game.bet_amount[self.user] == 100)
        self.assertTrue(self.game.bet_type[self.user])

    def test_reset(self):
        self.game.reset()
        self.assertTrue(self.game.bet_amount[self.user] == 0)
        self.assertTrue(self.game.payout[self.user] == 0)
        self.assertIsNone(self.game.bet_type[self.user])

    def test_remove_player(self):
        self.game.remove_player(self.user)
        self.assertEqual(0, len(self.game.bet_amount))
        self.assertEqual(0, len(self.game.payout))
        self.assertEqual(0, len(self.game.bet_type))

    def test_start_round_not_ready(self):
        self.game.wheel.result = -1
        self.game.bet_amount[self.user] = 0
        self.game.bet_type[self.user] = None
        self.game.start_round()

        self.assertEqual(self.game.wheel.result, -1)

    def test_start_round_ready(self):
        self.game.wheel.result = -1
        self.game.bet_amount[self.user] = 10
        self.game.bet_type[self.user] = {'type': 'odd'}
        self.game.start_round()

        self.assertTrue(self.game.all_ready())
        self.assertNotEqual(self.game.wheel.result, -1)

    def test_find_payout(self):
        self.game.wheel.result = '1'
        self.game.wheel.stage = 'ending'
        self.game.bet_amount[self.user] = 10.0
        self.game.bet_type[self.user] = {'type': 'odd'}
        self.game.find_payout()

        self.assertEqual(self.game.payout[self.user], 20.0)

    def test_check_bet_valid(self):
        self.assertTrue(self.game.check_bet_valid({'type': 'odd'}))
        self.assertTrue(self.game.check_bet_valid({'type': 'single', 'nums': ['0']}))
        self.assertFalse(self.game.check_bet_valid({'type': 'false'}))
        self.assertFalse(self.game.check_bet_valid({'type': 'single', 'nums': ['1', '2', '3']}))
        self.assertFalse(self.game.check_bet_valid({'type': 'single', 'nums': []}))


class TestWheel(TestCase):
    def setUp(self) -> None:
        CustomUser.objects.create_user(username='user', password='pass', current_balance=300)
        self.client.login(username='user', password='pass')
        self.user = auth.get_user(self.client)
        self.session_id = ROULETTE_MANAGER.create()
        ROULETTE_MANAGER.register_user(self.session_id, self.user)
        self.game = ROULETTE_MANAGER.get(self.session_id)

    def test_roll_stage(self):
        self.game.wheel.stage = 'ready'
        self.game.wheel.roll()
        self.assertEqual(self.game.wheel.get_stage(), 'ending')
        self.assertNotEqual(self.game.wheel.result, -1)

    def test_payout(self):
        self.game.wheel.result = '5'
        self.assertEqual(self.game.wheel.payout(10, {'type': 'even'}), 0)
        self.assertEqual(self.game.wheel.payout(10, {'type': 'odd'}), 20)


# class TestRouletteWebSocket(TestCase):
#     def setUp(self) -> None:
#         self.user = CustomUser.objects.create_user(username='user', password='pass', current_balance=1000)
#         self.user_two = CustomUser.objects.create_user(username='user_two', password='pass', current_balance=1000)
#         self.client.login(username='user', password='pass')
#         self.unique_id = ROULETTE_MANAGER.create()
#
#     def tearDown(self) -> None:
#         ROULETTE_MANAGER.sessions = {}
#
#     async def test_connects_to_websocket(self):
#         communicator = WebsocketCommunicator(application, "ws/roulette/{}/".format(self.unique_id))
#         communicator.scope['user'] = self.user
#         connected, _ = await communicator.connect()
#         self.assertTrue(connected)
#         await communicator.disconnect()
#
#     async def test_connects_to_websocket_from_limbo(self):
#         ROULETTE_MANAGER.get(self.unique_id).add_to_limbo(self.user)
#         communicator = WebsocketCommunicator(application, "ws/roulette/{}/".format(self.unique_id))
#         communicator.scope['user'] = self.user
#         connected, _ = await communicator.connect()
#         self.assertTrue(connected)
#         await communicator.disconnect()
#
#     async def test_disconnects_to_websocket_only_user_in_session(self):
#         communicator = WebsocketCommunicator(application, "ws/roulette/{}/".format(self.unique_id))
#         communicator.scope['user'] = self.user
#         connected, _ = await communicator.connect()
#         self.assertTrue(connected)
#         await communicator.disconnect()
#
#     async def test_disconnects_to_websocket_multiple_users_in_session(self):
#         communicator_1 = WebsocketCommunicator(application, "ws/roulette/{}/".format(self.unique_id))
#         communicator_1.scope['user'] = self.user
#         connected, _ = await communicator_1.connect()
#         self.assertTrue(connected)
#         communicator_2 = WebsocketCommunicator(application, "ws/roulette/{}/".format(self.unique_id))
#         communicator_2.scope['user'] = self.user_two
#         connected, _ = await communicator_2.connect()
#         self.assertTrue(connected)
#         await communicator_1.disconnect()
#         self.assertTrue(self.unique_id in ROULETTE_MANAGER.sessions.keys())
#         await communicator_2.disconnect()
#         self.assertTrue(self.unique_id not in ROULETTE_MANAGER.sessions.keys())
#
#     async def test_receive_play(self):
#         communicator = WebsocketCommunicator(application, "ws/roulette/{}/".format(self.unique_id))
#         communicator.scope['user'] = self.user
#         await communicator.connect()
#         await communicator.send_json_to({"type": "play"})
#         response = await communicator.receive_json_from()
#         self.assertEqual({'type': 'load_game',
#                           'data': {'players': [{'player': 'user', 'amount': '0.0', 'bet': 'null', 'payout': '0.0'}],
#                                    'result': -1, 'stage': 'betting'}, 'user': 'user'}, response)
#         await communicator.disconnect()
#
#     async def test_receive_place_bet(self):
#         communicator = WebsocketCommunicator(application, "ws/roulette/{}/".format(self.unique_id))
#         communicator.scope['user'] = self.user
#         await communicator.connect()
#         await communicator.send_json_to({
#             'type': 'place_bet',
#             'data': {'amount': 10, 'bet': {'type': 'even'}}
#         })
#         response = await communicator.receive_json_from()
#         self.assertEqual(10, float(response['data']['players'][0]['amount']))
#         await communicator.disconnect()
