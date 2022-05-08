from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.core.exceptions import ValidationError

from accounts.models import CustomUser


class CustomAuthenticationForm(AuthenticationForm):
    """
    Form for the custom login page
    """
    remember_me = forms.BooleanField(widget=forms.CheckboxInput(attrs={'value': 'remember-me'}), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control',
             'autofocus': '',
             'required': 'True'}
        )
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control',
             'required': 'True'}
        )


class CustomUserCreationForm(UserCreationForm):
    """
    Class defining the form for creating a user account. Includes typical username and password options, as well as
    first and last name, email address, account type (public or private), birthday, skill level, and a bio field.
    """
    email = forms.EmailField(required=True)
    account_type = forms.ChoiceField(choices=((0, 'Public'), (1, 'Private')), required=True)
    birthday = forms.DateField(required=True,
                               widget=forms.DateInput(attrs={
                                   'class': 'form-control',
                                   'type': 'date',
                               }))
    skill_level = forms.ChoiceField(
        choices=(('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('expert', 'Expert')), required=True)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    withdraw_limit = forms.FloatField(required=False)

    class Meta:
        """
        Overwriting existing configuration inherited from the UserCreationForm
        """
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email", "account_type", "birthday", "skill_level", "bio",
                  "password1", "password2", 'withdraw_limit')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['username', 'first_name', 'last_name', 'email', 'account_type', 'birthday', 'skill_level', 'bio',
                      'password1', 'password2', 'withdraw_limit']:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True) -> CustomUser:
        """
        Saves all the form data for a new user into the database

        Args:
            commit: boolean whether to commit the save

        Returns:
            the saved user
        """
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_private = self.cleaned_data["account_type"]
        user.birthday = self.cleaned_data["birthday"]
        user.skill_level = self.cleaned_data["skill_level"]
        user.bio = self.cleaned_data["bio"]
        if self.cleaned_data["withdraw_limit"]:
            user.monthly_limit = self.cleaned_data["withdraw_limit"]
            user.monthly_deposit_left = user.monthly_limit
            user.next_monthly_reset = datetime.now(timezone.utc) + relativedelta(months=1)

        if commit:
            user.save()
        return user


class CustomPasswordResetForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})


class AddFundsCryptoForm(forms.Form):
    """
    Class defining the form for adding funds to an account via a crypto wallet. The form requires a wallet address
    between 25 and 36 characters, as well as a dollar amount to add
    """

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AddFundsCryptoForm, self).__init__(*args, **kwargs)

    crypto_wallet_address = forms.CharField(max_length=36, min_length=25,
                                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    amount_to_add = forms.FloatField(min_value=0,
                                     widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean(self) -> dict:
        """
        Function responsible for validating the input of an AddFundsCryptoForm. Raises a ValidationError if any of the
        requirements for the form fields are not met

        Returns:
            a dictionary containing the form's valid input, self.cleaned_data
        """
        if self.user.monthly_limit > 0 and ((self.cleaned_data.get('amount_to_add') > self.user.monthly_deposit_left
                                             and self.user.next_monthly_reset > datetime.now(timezone.utc))
                                            or self.cleaned_data.get('amount_to_add') > self.user.monthly_limit):
            raise ValidationError("Surpassed Monthly Deposit Limit: You can deposit ${} more until {}".format(
                self.user.monthly_deposit_left, self.user.next_monthly_reset.strftime("%m/%d/%Y at %H:%M:%S UTC")))
        return self.cleaned_data


class AddFundsBankForm(forms.Form):
    """
    Class defining the form for adding funds to an account via a bank account. The form requires a routing number (a
    9-digit value which identifies the bank), as well as a 10-digit account number. A positive dollar amount to add is
    also required
    """

    routing_number = forms.IntegerField(widget=forms.TextInput(
        attrs={'pattern': '[0-9]{9}', 'title': "Routing number must be 9 digits", 'class': 'form-control'}))
    account_number = forms.IntegerField(min_value=0, widget=forms.TextInput(
        attrs={'pattern': '[0-9]{10}', 'title': "Account number must be 10 digits", 'class': 'form-control'}))
    amount_to_add = forms.FloatField(min_value=0,
                                     widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AddFundsBankForm, self).__init__(*args, **kwargs)

    def clean(self) -> dict:
        """
        Function responsible for validating the input of an AddFundsBankForm. Raises a ValidationError if any of the
        requirements for the form fields are not met

        Returns:
            a dictionary containing the form's valid input, self.cleaned_data
        """
        if len(str(self.cleaned_data.get('routing_number'))) != 9:
            raise ValidationError("Routing number is not 9 digits")

        if len(str(self.cleaned_data.get('account_number'))) != 10:
            raise ValidationError("Account number is not 10 digits")

        if self.user.monthly_limit > 0 and ((self.cleaned_data.get('amount_to_add') > self.user.monthly_deposit_left
                                             and self.user.next_monthly_reset > datetime.now(timezone.utc))
                                            or self.cleaned_data.get('amount_to_add') > self.user.monthly_limit):
            raise ValidationError("Surpassed Monthly Deposit Limit: You can deposit ${} more until {}".format(
                self.user.monthly_deposit_left, self.user.next_monthly_reset.strftime("%m/%d/%Y at %H:%M:%S UTC")))
        return self.cleaned_data


class WithdrawForm(forms.Form):
    """
    Class defining the form for withdrawing money from an account. The form requires a positive dollar amount to
    withdraw
    """

    def __init__(self, *args, **kwargs):
        self.current_balance = kwargs.pop('current_balance', 0)
        super(WithdrawForm, self).__init__(*args, **kwargs)

    amount_to_withdraw = forms.FloatField(min_value=0,
                                          widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean(self):
        """
        Function responsible for validating the input of a WithdrawForm. Raises a ValidationError if any of the
        requirements for the form fields are not met

        Returns:
            a dictionary containing the form's valid input, self.cleaned_data
        """
        if self.cleaned_data.get('amount_to_withdraw', float('inf')) > self.current_balance:
            raise ValidationError("Insufficient funds")
        return self.cleaned_data


class RequestForm(forms.Form):
    """
    Form for submitting a friend request
    """

    def __init__(self, *args, **kwargs):
        kwargs.pop('friend_requests', 0)
        super(RequestForm, self).__init__(*args, **kwargs)

    username = forms.CharField(max_length=36, min_length=1,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
