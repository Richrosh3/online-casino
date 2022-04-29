# from decimal import Decimal
#
# from django.contrib import auth
# from django.test import TestCase
#
# from accounts.models import CustomUser
# from games.slots.web.views import SLOTS_MANAGER
#
#
# class TestSlotsGame(TestCase):
#     """
#     Testing the Blackjack class
#     """
#
#     def setUp(self) -> None:
#         CustomUser.objects.create_user(username='user', password='pass', current_balance=Decimal(300))
#         self.client.login(username='user', password='pass')
#         self.user = auth.get_user(self.client)
#         self.session_id = SLOTS_MANAGER.create()
#         SLOTS_MANAGER.register_user(self.session_id, self.user)
#         self.game = SLOTS_MANAGER.get(self.session_id)
#
#     def tearDown(self) -> None:
#         SLOTS_MANAGER.sessions = {}
#
#     def test_record_bet(self):
#         self.game.bet = 50
#         self.game.record_bet(self.user)
#         self.user.refresh_from_db()
#         self.assertEqual(Decimal(250), self.user.current_balance)
#
#         self.game.bet = 100
#         self.game.record_bet(self.user)
#         self.user.refresh_from_db()
#         self.assertEqual(Decimal(150), self.user.current_balance)
#
#     def test_set_multiplier(self):
#         self.game.set_multiplier()
#         self.user.refresh_from_db()
#         self.assertTrue(0 < self.game.multiplier <= 5)
#
#     def test_play_slots(self):
#         outcome = self.game.play_slots()
#         self.assertEqual("spin", outcome['type'])
#         self.assertTrue(len(outcome['displayed_slots']) == 3)
#         self.assertTrue(outcome['payout'] >= 0)
#
#     def test_dict_representation(self):
#         self.assertEqual({'player': 'user', 'bet': 0, 'multiplier': 1}, self.game.dict_representation())
#
#
