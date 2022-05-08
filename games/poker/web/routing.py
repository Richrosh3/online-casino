from django.urls import re_path

from games.poker.web import consumers

websocket_urlpatterns = [
    re_path(r'ws/poker/(?P<session_id>[0-9a-f-]+)/$', consumers.PokerConsumer.as_asgi())
]
