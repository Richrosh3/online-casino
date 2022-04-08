from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from accounts.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    account_type = forms.ChoiceField(choices=((0, 'Public'), (1, 'Private')), required=True)
    email = forms.EmailField(required=True)
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
    amount_to_add = forms.DecimalField(decimal_places=2, min_value=0)


class AddFundsBankForm(forms.Form):
    routing_number = forms.IntegerField(widget=forms.TextInput(
        attrs={'pattern': '[0-9]{9}', 'title': "Routing number must be 9 digits"}))
    account_number = forms.IntegerField(min_value=0, widget=forms.TextInput(
        attrs={'pattern': '[0-9]*', 'title': "Enter a valid account number"}))
    amount_to_add = forms.DecimalField(decimal_places=2, min_value=0)

    def clean(self):
        if len(str(self.cleaned_data.get('routing_number'))) != 9:
            raise ValidationError("Routing number is not 9 digits")

        return self.cleaned_data


class WithdrawForm(forms.Form):
    amount_to_withdraw = forms.DecimalField(decimal_places=2, min_value=0)
