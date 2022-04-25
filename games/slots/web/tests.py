from decimal import Decimal

from django.contrib import auth
from django.test import TestCase

from accounts.models import CustomUser
from games.slots.web.views import SLOTS_MANAGER


class TestSlotsGame(TestCase):
    """
    Testing the Blackjack class
    """

    def setUp(self) -> None:
        CustomUser.objects.create_user(username='user', password='pass', current_balance=Decimal(300))
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
        self.assertEqual(Decimal(250), self.user.current_balance)
