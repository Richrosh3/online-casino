from django.urls import path

from games.roulette.web import views

urlpatterns = [
    path('session/<uuid:session_id>', views.RouletteSession.as_view(), name='roulette_game')
]