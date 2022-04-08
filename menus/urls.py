from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Games URLS
    path('games/', views.games, name='games'),
    path('games/poker_sessions/', views.current_poker_sessions, name='current_poker_sessions'),
    path('games/blackjack_sessions/', views.current_blackjack_sessions, name='current_blackjack_sessions'),
    path('games/craps_sessions/', views.current_craps_sessions, name='current_craps_sessions'),
    path('games/roulette_sessions/', views.current_roulette_sessions, name='current_roulette_sessions'),
    path('games/slots_sessions/', views.current_slots_sessions, name='current_slots_sessions')
]
