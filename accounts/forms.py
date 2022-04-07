from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    account_type = forms.ChoiceField(choices=((0, 'Public'), (1, 'Private')))

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_private = self.cleaned_data["account_type"]
        if commit:
            user.save()
        return user


class AddFundsCryptoForm(forms.Form):
    crypto_wallet_address = forms.CharField(max_length=36, min_length=25)
    amount_to_add = forms.DecimalField(decimal_places=2)

class WithdrawForm(forms.Form):
    amount_to_withdraw = forms.DecimalField(decimal_places=2)
    