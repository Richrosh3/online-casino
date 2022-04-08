from django.contrib import auth
from django.test import TestCase
from django.urls import reverse

from .models import CustomUser


class TestAccountFeatures(TestCase):
    """Feature tests for aspects of the account functionality. Tests logging in and out, adding and withdrawing funds,
    etc."""

    def test_create_user_and_logout_and_login(self):
        self.assertFalse(CustomUser.objects.filter(username='user').exists())
        signup_dict = {'username': 'user', 'email': 'user@umd.edu', 'password1': 'pass', 'password2': 'pass',
                       'account_type': 0}
        self.client.post(reverse('signup'), data=signup_dict)
        self.assertTrue(CustomUser.objects.filter(username='user').exists())

        self.client.get(reverse('logout'))
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

        login_dict = {'username': 'user', 'password': 'pass'}
        self.client.post(reverse('login'), data=login_dict)
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_deposit_and_withdraw(self):
        self.user = CustomUser.objects.create_user(username='user', password='pass', current_balance=1230.70)
        self.client.login(username='user', password='pass')

        bank_deposit_dict = {'routing_number': '123456789', 'account_number': '1234512345', 'amount_to_add': '125.00'}
        self.client.post(reverse('add_funds_bank'), data=bank_deposit_dict)
        self.user.refresh_from_db()
        self.assertEquals(float(self.user.current_balance), 1230.70 + 125.00)

        crypto_deposit_dict = {'crypto_wallet_address': '123456789123456789123456789', 'amount_to_add': '50.25'}
        self.client.post(reverse('add_funds_crypto'), data=crypto_deposit_dict)
        self.user.refresh_from_db()
        self.assertEquals(float(self.user.current_balance), 1230.70 + 125.00 + 50.25)

        withdraw_dict = {'amount_to_withdraw': '1000'}
        self.client.post(reverse('withdraw_funds'), data=withdraw_dict)
        self.user.refresh_from_db()
        self.assertEquals(float(self.user.current_balance), round(1230.70 + 125.00 + 50.25 - 1000, 2))
