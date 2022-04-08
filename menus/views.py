from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    """View function for the index page. Simply displays the index.html page.

    Args:
        request:    HttpRequest object, not used in this function

    Returns:
        An HttpResponse rendering the index.html page.
    """
    return render(request, 'menus/index.html')


@login_required
def games(request: HttpRequest) -> HttpResponse:
    """View function for the list of games page. Simply displays the games.html page.

    Args:
        request:    HttpRequest object, not used in this function

    Returns:
        An HttpResponse rendering the games.html page.
    """
    return render(request, 'menus/games.html')


@login_required
def current_poker_sessions(request: HttpRequest) -> HttpResponse:
    """View function for the Poker game page. Simply displays the poker.html page.

    Args:
        request:    HttpRequest object, not used in this function

    Returns:
        An HttpResponse rendering the poker.html page.
    """
    return render(request, 'menus/sessions/poker.html')


@login_required
def current_blackjack_sessions(request: HttpRequest) -> HttpResponse:
    """View function for the Blackjack game page. Simply displays the blackjack.html page.

    Args:
        request:    HttpRequest object, not used in this function

    Returns:
        An HttpResponse rendering the blackjack.html page.
    """
    return render(request, 'menus/sessions/blackjack.html')


@login_required
def current_craps_sessions(request: HttpRequest) -> HttpResponse:
    """View function for the Craps game page. Simply displays the craps.html page.

    Args:
        request:    HttpRequest object, not used in this function

    Returns:
        An HttpResponse rendering the craps.html page.
    """
    return render(request, 'menus/sessions/craps.html')


@login_required
def current_roulette_sessions(request: HttpRequest) -> HttpResponse:
    """View function for the Roulette game page. Simply displays the roulette.html page.

    Args:
        request:    HttpRequest object, not used in this function

    Returns:
        An HttpResponse rendering the roulette.html page.
    """
    return render(request, 'menus/sessions/roulette.html')


@login_required
def current_slots_sessions(request: HttpRequest) -> HttpResponse:
    """View function for the Slots game page. Simply displays the slots.html page.

    Args:
        request:    HttpRequest object, not used in this function

    Returns:
        An HttpResponse rendering the slots.html page.
    """
    return render(request, 'menus/sessions/slots.html')
