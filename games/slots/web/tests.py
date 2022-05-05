from channels.testing import WebsocketCommunicator
from django.contrib import auth
from django.test import TestCase

from OnlineCasino.asgi import application
from accounts.models import CustomUser
from games.slots.web.views import SLOTS_MANAGER


class TestSlotsGame(TestCase):
    """
    Testing the Blackjack class
    """

    def setUp(self) -> None:
        CustomUser.objects.create_user(username='user', password='pass', current_balance=300)
        self.client.login(username='user', password='pass')
        self.user = auth.get_user(self.client)
        self.session_id = SLOTS_MANAGER.create()
        SLOTS_MANAGER.register_user(self.session_id, self.user)
        self.game = SLOTS_MANAGER.get(self.session_id)

    def tearDown(self) -> None:
        SLOTS_MANAGER.sessions = {}

    def test_record_bet(self):
        self.game.bet = 50
        self.game.record_bet(self.user)
        self.user.refresh_from_db()
        self.assertEqual(250, self.user.current_balance)

        self.game.bet = 100
        self.game.record_bet(self.user)
        self.user.refresh_from_db()
        self.assertEqual(150, self.user.current_balance)

    def test_set_multiplier(self):
        self.game.set_multiplier()
        self.user.refresh_from_db()
        self.assertTrue(0 < self.game.multiplier <= 5)

    def test_play_slots(self):
        outcome = self.game.play_slots()
        self.assertEqual("spin", outcome['type'])
        self.assertTrue(len(outcome['displayed_slots']) == 3)
        self.assertTrue(outcome['payout'] >= 0)

    def test_dict_representation(self):
        self.assertEqual({'player': 'user', 'bet': 0, 'multiplier': 1}, self.game.dict_representation())


# class TestSlotsWebSocket(TestCase):
#     def setUp(self) -> None:
#         self.user = CustomUser.objects.create_user(username='user', password='pass', current_balance=1000)
#         self.user_two = CustomUser.objects.create_user(username='user_two', password='pass', current_balance=1000)
#         self.client.login(username='user', password='pass')
#         self.unique_id = SLOTS_MANAGER.create()
#
#     def tearDown(self) -> None:
#         SLOTS_MANAGER.sessions = {}
#
#     async def test_connects_to_websocket(self):
#         communicator = WebsocketCommunicator(application, "ws/slots/{}/".format(self.unique_id))
#         communicator.scope['user'] = self.user
#         connected, _ = await communicator.connect()
#         self.assertTrue(connected)
#         await communicator.disconnect()
#
#     async def test_connects_to_websocket_from_limbo(self):
#         SLOTS_MANAGER.get(self.unique_id).add_to_limbo(self.user)
#         communicator = WebsocketCommunicator(application, "ws/slots/{}/".format(self.unique_id))
#         communicator.scope['user'] = self.user
#         connected, _ = await communicator.connect()
#         self.assertTrue(connected)
#         await communicator.disconnect()
#
#     async def test_disconnects_to_websocket_only_user_in_session(self):
#         communicator = WebsocketCommunicator(application, "ws/slots/{}/".format(self.unique_id))
#         communicator.scope['user'] = self.user
#         connected, _ = await communicator.connect()
#         self.assertTrue(connected)
#         await communicator.disconnect()
#
#     async def test_disconnects_to_websocket_multiple_users_in_session(self):
#         communicator_1 = WebsocketCommunicator(application, "ws/slots/{}/".format(self.unique_id))
#         communicator_1.scope['user'] = self.user
#         connected, _ = await communicator_1.connect()
#         self.assertTrue(connected)
#         communicator_2 = WebsocketCommunicator(application, "ws/slots/{}/".format(self.unique_id))
#         communicator_2.scope['user'] = self.user_two
#         connected, _ = await communicator_2.connect()
#         self.assertTrue(connected)
#         await communicator_1.disconnect()
#         self.assertTrue(self.unique_id in SLOTS_MANAGER.sessions.keys())
#         await communicator_2.disconnect()
#         self.assertTrue(self.unique_id not in SLOTS_MANAGER.sessions.keys())
#
#     async def test_receive_load_game(self):
#         communicator = WebsocketCommunicator(application, "ws/slots/{}/".format(self.unique_id))
#         communicator.scope['user'] = self.user
#         await communicator.connect()
#         await communicator.send_json_to({"type": "load_game"})
#         response = await communicator.receive_json_from()
#         self.assertEqual({'type': 'load_game', 'data': {'player': 'user', 'bet': 0, 'multiplier': 1}, 'user': 'user'},
#                          response)
#         await communicator.disconnect()
#
#     async def test_receive_place_bet(self):
#         communicator = WebsocketCommunicator(application, "ws/slots/{}/".format(self.unique_id))
#         communicator.scope['user'] = self.user
#         await communicator.connect()
#         _ = await communicator.receive_json_from()
#         await communicator.send_json_to({"type": "place_bet", 'data': {'bet': 10}})
#         response = await communicator.receive_json_from()
#         self.assertEqual(10, float(response['data']['bet']))
#         await communicator.disconnect()
#
#     async def test_receive_play_slots(self):
#         communicator = WebsocketCommunicator(application, "ws/slots/{}/".format(self.unique_id))
#         communicator.scope['user'] = self.user
#         await communicator.connect()
#         _ = await communicator.receive_json_from()
#         await communicator.send_json_to({"type": "play_slots"})
#         response = await communicator.receive_json_from()
#         self.assertEqual('spin', response['type'])
#         await communicator.disconnect()
#
#     async def test_receive_player_balance(self):
#         communicator = WebsocketCommunicator(application, "ws/slots/{}/".format(self.unique_id))
#         communicator.scope['user'] = self.user
#         await communicator.connect()
#         _ = await communicator.receive_json_from()
#         await communicator.send_json_to({'type': 'request_user_balance'})
#         response = await communicator.receive_json_from()
#         self.assertEqual(self.user.current_balance, float(response['data']['balance']))
#         await communicator.disconnect()
