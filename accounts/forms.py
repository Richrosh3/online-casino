from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from accounts.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Class defining the form for creating a user account. Includes typical username and password options, as well as
    first and last name, email address, account type (public or private), birthday, skill level, and a bio field.
    """

    account_type = forms.ChoiceField(choices=((0, 'Public'), (1, 'Private')), required=True)
    email = forms.EmailField(required=True)
    birthday = forms.DateField(required=True,
                               widget=forms.DateInput(attrs={
                                   'placeholder': 'Birth Date',
                                   'class': 'form-control',
                                   'type': 'date',
                               }))
    skill_level = forms.ChoiceField(
        choices=(('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('expert', 'Expert')), required=True)
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        """
        Overwriting existing configuration inherited from the UserCreationForm
        """
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email", "account_type", "birthday", "skill_level", "bio",
                  "password1", "password2")

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

        if commit:
            user.save()
        return user


class AddFundsCryptoForm(forms.Form):
    """
    Class defining the form for adding funds to an account via a crypto wallet. The form requires a wallet address
    between 25 and 36 characters, as well as a dollar amount to add
    """

    crypto_wallet_address = forms.CharField(max_length=36, min_length=25)
    amount_to_add = forms.DecimalField(decimal_places=2, min_value=0)


class AddFundsBankForm(forms.Form):
    """
    Class defining the form for adding funds to an account via a bank account. The form requires a routing number (a
    9-digit value which identifies the bank), as well as a 10-digit account number. A positive dollar amount to add is
    also required
    """

    routing_number = forms.IntegerField(widget=forms.TextInput(
        attrs={'pattern': '[0-9]{9}', 'title': "Routing number must be 9 digits"}))
    account_number = forms.IntegerField(min_value=0, widget=forms.TextInput(
        attrs={'pattern': '[0-9]*{10}', 'title': "Account number must be 10 digits"}))
    amount_to_add = forms.DecimalField(decimal_places=2, min_value=0)

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

        return self.cleaned_data


class WithdrawForm(forms.Form):
    """
    Class defining the form for withdrawing money from an account. The form requires a positive dollar amount to
    withdraw
    """

    amount_to_withdraw = forms.DecimalField(decimal_places=2, min_value=0)
