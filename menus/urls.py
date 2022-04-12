from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),

    # Games URLS
    path('games/', views.Games.as_view(), name='games'),
    path('games/poker/', views.PokerSessions.as_view(), name='poker_sessions'),
    path('games/poker/', include('games.poker.web.urls')),
    path('games/blackjack/', include('games.blackjack.web.urls')),
    path('games/blackjack/', views.BlackjackSessions.as_view(), name='blackjack_sessions'),
    path('games/craps/', views.CrapsSessions.as_view(), name='craps_sessions'),
    path('games/craps/', include('games.craps.web.urls')),
    path('games/roulette/', views.RouletteSessions.as_view(), name='roulette_sessions'),
    path('games/roulette/', include('games.roulette.web.urls')),
    path('games/slots/', views.SlotsSessions.as_view(), name='slots_sessions'),
    path('games/slots/', include('games.slots.web.urls')),

]
