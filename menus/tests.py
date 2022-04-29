from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser


class TestIndexPage(TestCase):
    """
    Unit tests for the index page
    """

    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(username='user', password='pass')
        self.client.login(username='user', password='pass')

    def test_page_renders(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_no_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_games_menu_username_if_logged_in(self):
        response = self.client.get(reverse('index'))
        self.assertInHTML('Games'.format(self.user.username), response.content.decode())

    def test_displays_login_link_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('index'))
        self.assertInHTML('Login', response.content.decode())



class TestPokerPage(TestCase):
    """
    Unit tests for the Poker game page
    """

    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(username='user', password='pass')
        self.client.login(username='user', password='pass')

    def test_page_renders(self):
        response = self.client.get(reverse('poker_sessions'))
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('poker_sessions'))
        self.assertEqual(response.status_code, 302)


class TestBlackjackPage(TestCase):
    """
    Unit tests for the Blackjack game page
    """

    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(username='user', password='pass')
        self.client.login(username='user', password='pass')

    def test_page_renders(self):
        response = self.client.get(reverse('blackjack_sessions'))
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('blackjack_sessions'))
        self.assertEqual(response.status_code, 302)


class TestCrapsPage(TestCase):
    """
    Unit tests for the Craps game page
    """

    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(username='user', password='pass')
        self.client.login(username='user', password='pass')

    def test_page_renders(self):
        response = self.client.get(reverse('craps_sessions'))
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('craps_sessions'))
        self.assertEqual(response.status_code, 302)


class TestRoulettePage(TestCase):
    """
    Unit tests for the Roulette game page
    """

    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(username='user', password='pass')
        self.client.login(username='user', password='pass')

    def test_page_renders(self):
        response = self.client.get(reverse('roulette_sessions'))
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('roulette_sessions'))
        self.assertEqual(response.status_code, 302)


class TestSlotsPage(TestCase):
    """
    Unit tests for the Slots game page
    """

    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(username='user', password='pass')
        self.client.login(username='user', password='pass')

    def test_page_renders(self):
        response = self.client.get(reverse('slots_sessions'))
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('slots_sessions'))
        self.assertEqual(response.status_code, 302)
