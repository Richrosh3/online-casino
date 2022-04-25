from channels.routing import URLRouter
from django.urls import path

import games.blackjack.web.routing
import games.craps.web.routing
import games.poker.web.routing
import games.roulette.web.routing
import games.slots.web.routing

websocket_urlpatterns = [
    path('', URLRouter(games.slots.web.routing.websocket_urlpatterns)),
    path('', URLRouter(games.craps.web.routing.websocket_urlpatterns)),
    path('', URLRouter(games.poker.web.routing.websocket_urlpatterns)),
    path('', URLRouter(games.roulette.web.routing.websocket_urlpatterns)),
    path('', URLRouter(games.blackjack.web.routing.websocket_urlpatterns)),
]
