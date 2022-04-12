from channels.routing import URLRouter
from django.urls import path

import games.blackjack.web.routing
import games.craps.web.routing
import games.poker.web.routing
import games.roulette.web.routing
import games.slots.web.routing

websocket_urlpatterns = URLRouter([
    path('ws/', URLRouter(games.blackjack.web.routing.websocket_urlpatterns)),
    path('ws/', URLRouter(games.craps.web.routing.websocket_urlpatterns)),
    path('ws/', URLRouter(games.poker.web.routing.websocket_urlpatterns)),
    path('ws/', URLRouter(games.roulette.web.routing.websocket_urlpatterns)),
    path('ws/', URLRouter(games.slots.web.routing.websocket_urlpatterns)),
])
