from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, FormView

from accounts.forms import CustomUserCreationForm, AddFundsCryptoForm, WithdrawForm, AddFundsBankForm, \
    CustomAuthenticationForm, RequestForm
from accounts.models import CustomUser
from games.blackjack.web.views import BLACKJACK_MANAGER
from games.craps.web.views import CRAPS_MANAGER
from games.poker.web.views import POKER_MANAGER
from games.roulette.web.views import ROULETTE_MANAGER
from games.slots.web.views import SLOTS_MANAGER


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


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    redirect_authenticated_user = True

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            if not form.cleaned_data.get('remember_me', None):
                request.session.set_expiry(0)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AccountView(LoginRequiredMixin, TemplateView):
    """
    Class view for the Account game page. Simply displays the accounts.html page.
    """
    template_name = 'accounts/account.html'


class AddFundsBankView(LoginRequiredMixin, FormView):
    """
    Class view for the adding funds from bank account game page. Displays the html page and the form.
    """
    template_name = 'accounts/funds/add_from_bank.html'
    form_class = AddFundsBankForm

    def get_form_kwargs(self):
        """
        Passes user as parameter into AddFundsBankForm
        """
        kwargs = super(AddFundsBankView, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs

    def form_valid(self, form: AddFundsBankForm):
        self.request.user.deposit(form.cleaned_data['amount_to_add'])
        return redirect('account')


class AddFundsCryptoView(LoginRequiredMixin, FormView):
    """
    Class view for the adding funds from crypto wallet game page. Displays the html page and the form.
    """
    template_name = 'accounts/funds/add_from_crypto.html'
    form_class = AddFundsCryptoForm

    def get_form_kwargs(self) -> dict:
        """
        Passes user as parameter into AddFundsCryptoForm
        """
        kwargs = super(AddFundsCryptoView, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs

    def form_valid(self, form: AddFundsCryptoForm):
        self.request.user.deposit(form.cleaned_data['amount_to_add'])
        return redirect('account')


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
        form = WithdrawForm(request.POST, current_balance=request.user.current_balance)
        if form.is_valid():
            request.user.withdraw(float(request.POST['amount_to_withdraw']))
            return redirect('account')
    else:
        form = WithdrawForm()

    return render(request, 'accounts/funds/withdraw.html', {'form': form})


@login_required
def send_friend_request(request: WSGIRequest) -> HttpResponse:
    """
    Sends friend request to the username that is entered. 
    parameters: request containing the username in request.POST['username']
    returns: HttpResponse for which page to access
    """
    
    if request.method == 'POST':
        form = RequestForm(request.POST)
        request.user.send_friend_request(request.POST['username'])
        return redirect('friends')
    else:
        form = RequestForm()

    return render(request, 'accounts/send_requests.html', {'form': form})


@login_required
def accept_friend_request(request: WSGIRequest) -> HttpResponse:
    """
    Accepts a friend request from the accept request page. Redirects back to friends page after accepting request
    parameters: request containing the username in request.POST['username']
    returns: HttpResponse for which page to access
    """
    print(request.user.friend_requests)
    if request.method == 'POST':
        form = RequestForm(request.POST)

        request.user.accept_friend_request(request.POST['username'])

        return redirect('friends')
    else:
        form = RequestForm()

    return render(request, 'accounts/accept_requests.html', {'form': form})


@login_required
def remove_friend(request: WSGIRequest) -> HttpResponse:
    """
    Removes friend from the user's friends. Renders remove page if accessed from my friends page,
    otherwise redirects back to friends page after entering response on remove page
    parameters: request containing the username in request.POST['username']
    returns: HttpResponse for which page to access

    """
    if request.method == 'POST':
        form = RequestForm(request.POST)
        request.user.remove_friend(request.POST['username'])
        return redirect('friends')

    else:
        form = RequestForm()

    return render(request, 'accounts/remove_friends.html', {'form': form})



@login_required
def friends_view(request: WSGIRequest):
    if request.method == 'GET':
        friends = request.user.friends.all()

        friends_list = dict()
        for friend in friends:
            for manager in [BLACKJACK_MANAGER, CRAPS_MANAGER, POKER_MANAGER, ROULETTE_MANAGER, SLOTS_MANAGER]:
                session = manager.get_players_game(friend)
                if session is not None:
                    if manager.game in ['blackjack', 'craps', 'poker']:
                        friends_list[friend] = "{}/session/{}".format(manager.game, str(session))
                    else:
                        friends_list[friend] = "{}/session/{}?spectate=true".format(manager.game, str(session))
                    break
        return render(request, 'accounts/friends.html', context={'friends_list': friends_list})


class FriendsView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/friends.html'
