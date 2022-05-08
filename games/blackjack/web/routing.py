from django.urls import re_path

from games.blackjack.web import consumers

websocket_urlpatterns = [
    re_path(r'ws/blackjack/(?P<session_id>[0-9a-f-]+)/$', consumers.BlackjackConsumer.as_asgi())
]
