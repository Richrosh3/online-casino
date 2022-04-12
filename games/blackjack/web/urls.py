from django.urls import path

from games.blackjack.web import views

urlpatterns = [
    path('session/<uuid:session>', views.BlackjackSession.as_view(), name='blackjack_game')
]
