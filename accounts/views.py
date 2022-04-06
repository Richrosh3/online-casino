import decimal

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import CustomUserCreationForm, AddFundsCryptoForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("index")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect('index')


@login_required
def account(request):
    return render(request, 'accounts/account.html')


@login_required
def add_funds_bank(request):
    return render(request, 'accounts/funds/add_from_bank.html')


@login_required
def add_funds_crypto(request):
    if request.method == 'POST':
        request.user.current_balance += decimal.Decimal(request.POST['amount_to_add'])
        request.user.save()
        return redirect('account')

    return render(request, 'accounts/funds/add_from_crypto.html', {'form': AddFundsCryptoForm()})


@login_required
def withdraw_funds(request):
    return render(request, 'accounts/funds/withdraw.html')
