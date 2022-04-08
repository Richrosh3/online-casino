from decimal import Decimal

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import CustomUserCreationForm, AddFundsCryptoForm, WithdrawForm, AddFundsBankForm


class SignUpView(CreateView):
    """
    Class representing the view for the signup page. Uses the CustomUserCreationForm defined in forms.py, and
    redirects to the index page upon submission and processing of the form.
    """

    form_class = CustomUserCreationForm
    success_url = reverse_lazy("index")
    template_name = "registration/signup.html"

    def form_valid(self, form: CustomUserCreationForm) -> HttpResponse:
        """
        Validates the CustomUserCreationForm. Then creates a user with the specified information, logs them in, and
        redirects to the index page if the form is valid.

        Args:
            form:   the complete CustomUserCreationForm form to be validated

        Returns:
            An HttpResponse redirecting to index
        """
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect('index')


@login_required
def account(request: WSGIRequest) -> HttpResponse:
    """
    View function for the account page. Simply displays the account.html page.

    Args:
        request:    WSGIRequest object containing the request information

    Returns:
        An HttpResponse rendering the account.html page.
    """
    return render(request, 'accounts/account.html')


@login_required
def add_funds_bank(request: WSGIRequest) -> HttpResponse:
    """
    View function for the add funds via bank page. For a valid POST request, the appropriate funds will be added to
    the user's account and the user will be redirected to the account page.

    Args:
        request:    WSGIRequest object containing the request information

    Returns:
        For a POST request, returns an HttpResponse object redirecting back to the account page.
        Otherwise, returns an HttpResponse object rendering the add_from_bank.html page with an AddFundsBankForm.
    """
    if request.method == 'POST':
        form = AddFundsBankForm(request.POST)
        if form.is_valid():
            request.user.update_balance(Decimal(request.POST['amount_to_add']))
            return redirect('account')

    return render(request, 'accounts/funds/add_from_bank.html', {'form': AddFundsBankForm()})


@login_required
def add_funds_crypto(request: WSGIRequest) -> HttpResponse:
    """
    View function for the add funds via crypto page. For a valid POST request, the appropriate funds will be added to
    the user's account and the user will be redirected to the account page.

    Args:
        request:    WSGIRequest object containing the request information

    Returns:
        For a POST request, returns an HttpResponse object redirecting back to the account page.
        Otherwise, returns an HttpResponse object rendering the add_from_crypto.html page with an AddFundsCryptoForm.
    """
    if request.method == 'POST':
        form = AddFundsCryptoForm(request.POST)
        if form.is_valid():
            request.user.update_balance(Decimal(request.POST['amount_to_add']))
            return redirect('account')

    return render(request, 'accounts/funds/add_from_crypto.html', {'form': AddFundsCryptoForm()})


@login_required
def withdraw_funds(request: WSGIRequest) -> HttpResponse:
    """
    View function for the withdraw funds page. For a valid POST request, the appropriate funds will be removed from the
    account and the user will be redirected to the account page.

    Args:
        request:    WSGIRequest object containing the request information

    Returns:
        For a POST request, returns an HttpResponse object redirecting back to the account page.
        Otherwise, returns an HttpResponse object rendering the withdraw.html page with a WithdrawForm.
    """
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            if request.user.current_balance >= Decimal(request.POST['amount_to_withdraw']):
                request.user.update_balance(-Decimal(request.POST['amount_to_withdraw']))
            return redirect('account')

    return render(request, 'accounts/funds/withdraw.html', {'form': WithdrawForm()})
