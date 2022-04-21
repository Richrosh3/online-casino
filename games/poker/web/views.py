from django.shortcuts import render
from games.base import SessionManager, GameSessionView
from games.poker.game.poker import Poker

POKER_MANAGER = SessionManager(Poker)


# Create your views here.

class PokerSession(GameSessionView):
    template_name = 'poker/poker.html'
    game_manager = POKER_MANAGER
    redirect_to = 'poker_sessions'




