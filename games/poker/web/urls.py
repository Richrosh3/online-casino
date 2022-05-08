from django.urls import path

from games.poker.web import views

urlpatterns = [
    path('session/<uuid:session>', views.PokerSession.as_view(), name='poker_game')
]
