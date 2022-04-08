from decimal import Decimal

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import CustomUserCreationForm, AddFundsCryptoForm, WithdrawForm, AddFundsBankForm


class SignUpView(CreateView):
    """Class representing the view for the signup page. Uses the CustomUserCreationForm defined in forms.py, and
    redirects to the index page upon submission and processing of the form."""

    form_class = CustomUserCreationForm
    success_url = reverse_lazy("index")
    template_name = "registration/signup.html"

    def form_valid(self, form: CustomUserCreationForm) -> HttpResponse:
        """Function called when the form is POSTed. Creates a user with the specified username and password, logs that
        user in, and redirects to index.html

        Args:
            form:   the form being validated; contains the information representing the new user being created.

        Returns:
            An HttpResponse redirecting to index.html
        """
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect('index')


@login_required
def account(request: HttpRequest) -> HttpResponse:
    """View function for the account page. Simply displays the account.html page.

    Args:
        request:    HttpRequest object, not used in this function

    Returns:
        An HttpResponse rendering the account.html page.
    """
    return render(request, 'accounts/account.html')


@login_required
def add_funds_bank(request: HttpRequest) -> HttpResponse:
    """View function for the add funds via bank page. If data has been POSTed, and it is valid, then the appropriate
    funds will be added to the account.

    Args:
        request:    HttpRequest object containing the request information. Will contain the information from the form
                    when it is submitted.

    Returns:
        If there is data being POSTed, return an HttpResponse object redirecting back to the account.html page.
        Otherwise, an HttpResponse object rendering the add_from_bank.html page with an AddFundsBankForm is returned.
    """
    if request.method == 'POST':
        form = AddFundsBankForm(request.POST)
        if form.is_valid():
            request.user.update_balance(Decimal(request.POST['amount_to_add']))
            return redirect('account')

    return render(request, 'accounts/funds/add_from_bank.html', {'form': AddFundsBankForm()})


@login_required
def add_funds_crypto(request: HttpRequest) -> HttpResponse:
    """View function for the add funds via crypto page. If data has been POSTed, and it is valid, then the appropriate
    funds will be added to the account.

    Args:
        request:    HttpRequest object containing the request information. Will contain the information from the form
                    when it is submitted.

    Returns:
        If there is data being POSTed, return an HttpResponse object redirecting back to the account.html page.
        Otherwise, an HttpResponse object rendering the add_from_crypto.html page with an AddFundsCryptoForm is
        returned.
    """
    if request.method == 'POST':
        form = AddFundsCryptoForm(request.POST)
        if form.is_valid():
            request.user.update_balance(Decimal(request.POST['amount_to_add']))
            return redirect('account')

    return render(request, 'accounts/funds/add_from_crypto.html', {'form': AddFundsCryptoForm()})


@login_required
def withdraw_funds(request: HttpRequest) -> HttpResponse:
    """View function for the withdraw funds page. If data has been POSTed, and it is valid, then the appropriate funds
    will be removed from the account.

    Args:
        request:    HttpRequest object containing the request information. Will contain the information from the form
                    when it is submitted.

    Returns:
        If there is data being POSTed, return an HttpResponse object redirecting back to the account.html page.
        Otherwise, an HttpResponse object rendering the withdraw.html page with a WithdrawForm is returned.
    """
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            if request.user.current_balance >= Decimal(request.POST['amount_to_withdraw']):
                request.user.update_balance(-Decimal(request.POST['amount_to_withdraw']))
            return redirect('account')

    return render(request, 'accounts/funds/withdraw.html', {'form': WithdrawForm()})
