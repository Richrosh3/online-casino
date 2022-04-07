from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def index(request):
    return render(request, 'menus/index.html')


@login_required
def games(request):
    return render(request, 'menus/games.html')


@login_required
def current_poker_sessions(request):
    return render(request, 'menus/sessions/poker.html')


@login_required
def current_blackjack_sessions(request):
    return render(request, 'menus/sessions/blackjack.html')


@login_required
def current_craps_sessions(request):
    return render(request, 'menus/sessions/craps.html')


@login_required
def current_roulette_sessions(request):
    return render(request, 'menus/sessions/roulette.html')


@login_required
def current_slots_sessions(request):
    return render(request, 'menus/sessions/slots.html')
