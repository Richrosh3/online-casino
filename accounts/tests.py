from django.contrib import auth
from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser


class TestSignupPage(TestCase):
    """Unit tests for the signup page."""

    def test_page_renders(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_invalid_email_address(self):
        payload = {'username': 'user', 'email': 'not_an_email', 'password1': 'pass', 'password2': 'pass',
                   'account_type': 0}
        self.client.post(reverse('signup'), data=payload)
        self.assertFalse(CustomUser.objects.filter(username='user').exists())

    def test_empty_email_address(self):
        payload = {'username': 'user', 'email': '', 'password1': 'pass', 'password2': 'pass',
                   'account_type': 0}
        self.client.post(reverse('signup'), data=payload)
        self.assertFalse(CustomUser.objects.filter(username='user').exists())

    def test_dict_missing_email_address(self):
        payload = {'username': 'user', 'password1': 'pass', 'password2': 'pass',
                   'account_type': 0}
        self.client.post(reverse('signup'), data=payload)
        self.assertFalse(CustomUser.objects.filter(username='user').exists())

    def test_empty_username(self):
        payload = {'username': '', 'email': 'test@gmail.com', 'password1': 'pass', 'password2': 'pass',
                   'account_type': 0}
        self.client.post(reverse('signup'), data=payload)
        self.assertFalse(CustomUser.objects.filter(username='user').exists())

    def test_dict_missing_username(self):
        payload = {'email': 'test@gmail.com', 'password1': 'pass', 'password2': 'pass',
                   'account_type': 0}
        self.client.post(reverse('signup'), data=payload)
        self.assertFalse(CustomUser.objects.filter(username='user').exists())

    def test_duplicate_username(self):
        new_user = CustomUser.objects.create(username='user')
        payload = {'username': 'user', 'email': '', 'password1': 'pass', 'password2': 'pass',
                   'account_type': 0}
        self.client.post(reverse('signup'), data=payload)
        queried_user = CustomUser.objects.get(username='user')
        self.assertEquals(new_user, queried_user)

    def test_empty_password1(self):
        payload = {'username': 'user', 'email': 'test@gmail.com', 'password1': '', 'password2': 'pass',
                   'account_type': 0}
        self.client.post(reverse('signup'), data=payload)
        self.assertFalse(CustomUser.objects.filter(username='user').exists())

    def test_dict_missing_password1(self):
        payload = {'username': 'user', 'email': 'test@gmail.com', 'password2': 'pass', 'account_type': 0}
        self.client.post(reverse('signup'), data=payload)
        self.assertFalse(CustomUser.objects.filter(username='user').exists())

    def test_empty_password2(self):
        payload = {'username': 'user', 'email': 'test@gmail.com', 'password1': 'pass', 'password2': '',
                   'account_type': 0}
        self.client.post(reverse('signup'), data=payload)
        self.assertFalse(CustomUser.objects.filter(username='user').exists())

    def test_dict_missing_password2(self):
        payload = {'username': 'user', 'email': 'test@gmail.com', 'password1': 'pass', 'account_type': 0}
        self.client.post(reverse('signup'), data=payload)
        self.assertFalse(CustomUser.objects.filter(username='user').exists())

    def test_empty_both_passwords(self):
        payload = {'username': 'user', 'email': 'test@gmail.com', 'password1': '', 'password2': '',
                   'account_type': 0}
        self.client.post(reverse('signup'), data=payload)
        self.assertFalse(CustomUser.objects.filter(username='user').exists())

    def test_passwords_do_not_match(self):
        payload = {'username': 'user', 'email': 'test@gmail.com', 'password1': 'pass', 'password2': 'not_pass',
                   'account_type': 0}
        self.client.post(reverse('signup'), data=payload)
        self.assertFalse(CustomUser.objects.filter(username='user').exists())

    def test_invalid_account_type(self):
        payload = {'username': 'user', 'email': '', 'password1': 'pass', 'password2': 'pass',
                   'account_type': -1}
        self.client.post(reverse('signup'), data=payload)
        self.assertFalse(CustomUser.objects.filter(username='user').exists())

    def test_dict_missing_account_type(self):
        payload = {'username': 'user', 'email': '', 'password1': 'pass', 'password2': 'pass'}
        self.client.post(reverse('signup'), data=payload)
        self.assertFalse(CustomUser.objects.filter(username='user').exists())

    def test_valid_create_request(self):
        payload = {'username': 'user', 'email': 'user@umd.edu', 'password1': 'pass', 'password2': 'pass',
                   'account_type': 0}
        self.client.post(reverse('signup'), data=payload)
        self.assertTrue(CustomUser.objects.filter(username='user').exists())


class TestLoginPage(TestCase):
    """Unit tests for the login page."""

    def setUp(self) -> None:
        CustomUser.objects.create_user(username='user', password='pass')

    def test_page_renders(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_empty_username(self):
        payload = {'username': '', 'password': 'pass'}
        self.client.post(reverse('login'), data=payload)
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_dict_missing_username(self):
        payload = {'password': 'pass'}
        self.client.post(reverse('login'), data=payload)
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_empty_password(self):
        payload = {'username': 'user', 'password': ''}
        self.client.post(reverse('login'), data=payload)
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_dict_missing_password(self):
        payload = {'username': 'user'}
        self.client.post(reverse('login'), data=payload)
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_non_existent_username(self):
        payload = {'username': 'not_user', 'password': 'pass'}
        self.client.post(reverse('login'), data=payload)
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_incorrect_password(self):
        payload = {'username': 'user', 'password': 'not_pass'}
        self.client.post(reverse('login'), data=payload)
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_correct_credentials_succeeds(self):
        payload = {'username': 'user', 'password': 'pass'}
        self.client.post(reverse('login'), data=payload)
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

        self.assertTrue(self.client.login(username='user', password='pass'))

    def test_auto_logs_in_upon_signup(self):
        payload = {'username': 'user', 'password': 'pass'}
        self.client.post(reverse('login'), data=payload)
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_redirect_to_index_if_already_logged_in(self):
        self.client.login(username='user', password='pass')
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)


class TestLogout(TestCase):
    """Unit tests for logging out of accounts."""

    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(username='user', password='pass', current_balance=123.40,
                                                   total_earnings=543.20)
        self.client.login(username='user', password='pass')

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 302)

    def test_logout_if_logged_in(self):
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)


class TestMyAccountPage(TestCase):
    """Unit tests for the account page."""

    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(username='user', password='pass', current_balance=123.40,
                                                   total_earnings=543.20)
        self.client.login(username='user', password='pass')

    def test_page_renders(self):
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 302)

    def test_displays_correct_account_balance(self):
        response = self.client.get(reverse('account'))
        self.assertInHTML('Your current account balance is {:.2f}'.format(self.user.current_balance),
                          response.content.decode())

    def test_displays_correct_total_earnings(self):
        response = self.client.get(reverse('account'))
        self.assertInHTML('Your total earnings is {:.2f}'.format(self.user.total_earnings),
                          response.content.decode())


class TestAddingFundsFromBank(TestCase):
    """Unit tests for adding funds from a bank account."""

    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(username='user', password='pass', current_balance=123.40,
                                                   total_earnings=543.20)
        self.client.login(username='user', password='pass')

    def test_page_renders(self):
        response = self.client.get(reverse('add_funds_bank'))
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('add_funds_bank'))
        self.assertEqual(response.status_code, 302)

    def test_routing_number_not_all_digits_fails(self):
        payload = {'routing_number': '12abc6789', 'account_number': '1234512345', 'amount_to_add': '10'}
        self.client.post(reverse('add_funds_bank'), data=payload)
        self.user.refresh_from_db()
        self.assertEquals(float(self.user.current_balance), 123.40)

    def test_routing_number_not_correct_length_fails(self):
        payload = {'routing_number': '12345', 'account_number': '1234512345', 'amount_to_add': '10'}
        self.client.post(reverse('add_funds_bank'), data=payload)
        self.user.refresh_from_db()
        self.assertEquals(float(self.user.current_balance), 123.40)

    def test_routing_number_not_in_dict_fails(self):
        payload = {'account_number': '1234512345', 'amount_to_add': '10'}
        self.client.post(reverse('add_funds_bank'), data=payload)
        self.user.refresh_from_db()
        self.assertEquals(float(self.user.current_balance), 123.40)

    def test_account_number_not_all_digits_fails(self):
        payload = {'routing_number': '123456789', 'account_number': '123abc1231', 'amount_to_add': '10'}
        self.client.post(reverse('add_funds_bank'), data=payload)
        self.user.refresh_from_db()
        self.assertEquals(float(self.user.current_balance), 123.40)

    def test_account_number_not_correct_length_fails(self):
        payload = {'routing number': '123456789', 'account_number': '12345', 'amount_to_add': '10'}
        self.client.post(reverse('add_funds_bank'), data=payload)
        self.user.refresh_from_db()
        self.assertEquals(float(self.user.current_balance), 123.40)

    def test_negative_account_number_fails(self):
        payload = {'routing_number': '123456789', 'account_number': '-1234512345', 'amount_to_add': '10'}
        self.client.post(reverse('add_funds_bank'), data=payload)
        self.user.refresh_from_db()
        self.assertEquals(float(self.user.current_balance), 123.40)

    def test_account_number_not_in_dict_fails(self):
        payload = {'routing_number': '123456789', 'amount_to_add': '10'}
        self.client.post(reverse('add_funds_bank'), data=payload)
        self.user.refresh_from_db()
        self.assertEquals(float(self.user.current_balance), 123.40)

    def test_negative_deposit_amount_fails(self):
        payload = {'routing_number': '123456789', 'account_number': '1234512345', 'amount_to_add': '-10'}
        self.client.post(reverse('add_funds_bank'), data=payload)
        self.user.refresh_from_db()
        self.assertEquals(float(self.user.current_balance), 123.40)

    def test_deposit_amount_not_a_number_fails(self):
        payload = {'routing_number': '123456789', 'account_number': '1234512345', 'amount_to_add': '1ac0'}
        self.client.post(reverse('add_funds_bank'), data=payload)
        self.user.refresh_from_db()
        self.assertEquals(float(self.user.current_balance), 123.40)

    def test_amount_to_add_not_in_dict_fails(self):
        payload = {'routing_number': '123456789', 'account_number': '1234512345'}
        self.client.post(reverse('add_funds_bank'), data=payload)
        self.user.refresh_from_db()
        self.assertEquals(float(self.user.current_balance), 123.40)

    def test_correct_form_adds_to_balance(self):
        payload = {'routing_number': '123456789', 'account_number': '1234512345', 'amount_to_add': '125.79'}
        self.client.post(reverse('add_funds_bank'), data=payload)
        self.user.refresh_from_db()
        self.assertEquals(float(self.user.current_balance), 123.40 + 125.79)


class TestAddingFundsFromCrypto(TestCase):
    """Unit tests for adding funds from a crypto wallet."""

    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(username='user', password='pass', current_balance=123.40,
                                                   total_earnings=543.20)
        self.client.login(username='user', password='pass')

    def test_page_renders(self):
        response = self.client.get(reverse('add_funds_crypto'))
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('add_funds_crypto'))
        self.assertEqual(response.status_code, 302)

    def test_wallet_address_too_long_fails(self):
        payload = {'crypto_wallet_address': '1234567891234567891234567891234567891', 'amount_to_add': '10'}
        self.client.post(reverse('add_funds_crypto'), data=payload)
        self.user.refresh_from_db()
        self.assertEquals(float(self.user.current_balance), 123.40)

    def test_wallet_address_too_short_fails(self):
        payload = {'crypto_wallet_address': '123456789123456789123456', 'amount_to_add': '10'}
        self.client.post(reverse('add_funds_crypto'), data=payload)
        self.user.refresh_from_db()
        self.assertEquals(float(self.user.current_balance), 123.40)

    def test_wallet_address_not_in_dict_fails(self):
        payload = {'amount_to_add': '10'}
        self.client.post(reverse('add_funds_crypto'), data=payload)
        self.user.refresh_from_db()
        self.assertEquals(float(self.user.current_balance), 123.40)

    def test_negative_deposit_amount_fails(self):
        payload = {'crypto_wallet_address': '123456789123456789123456789', 'amount_to_add': '-10'}
        self.client.post(reverse('add_funds_crypto'), data=payload)
        self.user.refresh_from_db()
        self.assertEquals(float(self.user.current_balance), 123.40)

    def test_deposit_amount_not_a_number_fails(self):
        payload = {'crypto_wallet_address': '123456789123456789123456789', 'amount_to_add': '1ac0'}
        self.client.post(reverse('add_funds_crypto'), data=payload)
        self.user.refresh_from_db()
        self.assertEquals(float(self.user.current_balance), 123.40)

    def test_amount_to_add_not_in_dict_fails(self):
        payload = {'crypto_wallet_address': '123456789123456789123456789'}
        self.client.post(reverse('add_funds_crypto'), data=payload)
        self.user.refresh_from_db()
        self.assertEquals(float(self.user.current_balance), 123.40)

    def test_correct_form_adds_to_balance(self):
        payload = {'crypto_wallet_address': '123456789123456789123456789', 'amount_to_add': '125.79'}
        self.client.post(reverse('add_funds_crypto'), data=payload)
        self.user.refresh_from_db()
        self.assertEquals(float(self.user.current_balance), 123.40 + 125.79)


class TestWithdrawFunds(TestCase):
    """Unit tests for withdrawing funds from an account."""

    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(username='user', password='pass', current_balance=123.40,
                                                   total_earnings=543.20)
        self.client.login(username='user', password='pass')

    def test_page_renders(self):
        response = self.client.get(reverse('withdraw_funds'))
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('withdraw_funds'))
        self.assertEqual(response.status_code, 302)

    def test_displays_correct_account_balance(self):
        response = self.client.get(reverse('withdraw_funds'))
        self.assertInHTML('Current Balance:  {:.2f}'.format(self.user.current_balance),
                          response.content.decode())

    def test_negative_withdraw_amount_fails(self):
        payload = {'amount_to_withdraw': '-10'}
        self.client.post(reverse('withdraw_funds'), data=payload)
        self.user.refresh_from_db()
        self.assertEquals(float(self.user.current_balance), 123.40)

    def test_deposit_amount_not_a_number_fails(self):
        payload = {'amount_to_withdraw': '1ac0'}
        self.client.post(reverse('withdraw_funds'), data=payload)
        self.user.refresh_from_db()
        self.assertEquals(float(self.user.current_balance), 123.40)

    def test_amount_to_add_not_in_dict_fails(self):
        payload = {}
        self.client.post(reverse('withdraw_funds'), data=payload)
        self.user.refresh_from_db()
        self.assertEquals(float(self.user.current_balance), 123.40)

    def test_correct_form_adds_to_balance(self):
        payload = {'amount_to_withdraw': '100.79'}
        self.client.post(reverse('withdraw_funds'), data=payload)
        self.user.refresh_from_db()
        self.assertEquals(float(self.user.current_balance), 123.40 - 100.79)
