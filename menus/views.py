from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView
from games.poker.web.views import POKER_MANAGER
from games.craps.web.views import CRAPS_MANAGER
from games.roulette.web.views import ROULETTE_MANAGER
from games.blackjack.web.views import BLACKJACK_MANAGER
from games.slots.web.views import SLOTS_MANAGER


class Index(TemplateView):
    """
    Class view for the index page. Simply displays the index.html page.
    """
    template_name = 'menus/index.html'


class Games(LoginRequiredMixin, TemplateView):
    """
    Class view for the list of games page. Simply displays the games.html page.
    """
    template_name = 'menus/games.html'


class PokerSessions(LoginRequiredMixin, TemplateView):
    """
    Class view for the Poker game page. Simply displays the poker.html page.
    """
    template_name = 'menus/sessions/poker.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['sessions'] = POKER_MANAGER.list_sessions()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests
        """
        unique_id = POKER_MANAGER.create()
        return redirect('poker_game', session=unique_id)


class BlackjackSessions(LoginRequiredMixin, TemplateView):
    """
    Class view for the Blackjack game page. Simply displays the blackjack.html page.
    """
    template_name = 'menus/sessions/blackjack.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['sessions'] = BLACKJACK_MANAGER.list_sessions()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests
        """
        unique_id = BLACKJACK_MANAGER.create()
        return redirect('blackjack_game', session=unique_id)


class CrapsSessions(LoginRequiredMixin, TemplateView):
    """
    Class view for the Craps game page. Simply displays the craps.html page.
    """
    template_name = 'menus/sessions/craps.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['sessions'] = CRAPS_MANAGER.list_sessions()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests
        """
        unique_id = CRAPS_MANAGER.create()
        return redirect('craps_game', session=unique_id)


class RouletteSessions(LoginRequiredMixin, TemplateView):
    """
    Class view for the Roulette game page. Simply displays the roulette.html page.
    """
    template_name = 'menus/sessions/roulette.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['sessions'] = ROULETTE_MANAGER.list_sessions()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests
        """
        unique_id = ROULETTE_MANAGER.create()
        return redirect('roulette_game', session=unique_id)


class SlotsSessions(LoginRequiredMixin, TemplateView):
    """
    Class view for the Roulette game page. Simply displays the roulette.html page.
    """
    template_name = 'menus/sessions/slots.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['sessions'] = SLOTS_MANAGER.list_sessions()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests
        """
        unique_id = SLOTS_MANAGER.create()
        return redirect('slots_game', session=unique_id)
