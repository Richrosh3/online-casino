from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    account_type = forms.ChoiceField(choices=((0, 'Public'), (1, 'Private')))
    birthday = forms.DateField(required=True,
                               widget=forms.DateInput(attrs={
                                   'placeholder': 'Birth Date',
                                   'class': 'form-control',
                                   'type': 'date',
                               }))
    skill_level = forms.ChoiceField(choices=((0, 'Beginner'), (1, 'Intermediate'), (2, 'Expert')))
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email", "account_type", "birthday", "skill_level", "bio",
                  "password1", "password2")

    def save(self, commit=True):
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
    crypto_wallet_address = forms.CharField(max_length=36, min_length=25)
    amount_to_add = forms.DecimalField(decimal_places=2)


class WithdrawForm(forms.Form):
    amount_to_withdraw = forms.DecimalField(decimal_places=2)
