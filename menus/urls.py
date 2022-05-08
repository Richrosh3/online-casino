from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),

    # Games URLS
    path('games/poker/', views.PokerSessions.as_view(), name='poker_sessions'),
    path('games/poker/', include('games.poker.web.urls')),
    path('tutorials/poker/', views.PokerRules.as_view(), name='poker_rules'),

    path('games/blackjack/', include('games.blackjack.web.urls')),
    path('games/blackjack/', views.BlackjackSessions.as_view(), name='blackjack_sessions'),
    path('tutorials/blackjack/', views.BlackjackRules.as_view(), name='blackjack_rules'),

    path('games/craps/', views.CrapsSessions.as_view(), name='craps_sessions'),
    path('games/craps/', include('games.craps.web.urls')),
    path('tutorials/craps/', views.CrapsRules.as_view(), name='craps_rules'),

    path('games/roulette/', views.RouletteSessions.as_view(), name='roulette_sessions'),
    path('games/roulette/', include('games.roulette.web.urls')),
    path('tutorials/roulette/', views.RouletteRules.as_view(), name='roulette_rules'),

    path('games/slots/', views.SlotsSessions.as_view(), name='slots_sessions'),
    path('games/slots/', include('games.slots.web.urls')),

    path('sessions/', views.GameSessions.as_view(), name='sessions'),

    path('tutorials/slots/', views.SlotsRules.as_view(), name='slots_rules')
]
