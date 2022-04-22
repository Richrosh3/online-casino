from django.urls import re_path
from games.roulette.web import consumers

websocket_urlpatterns = [
    re_path(r'ws/roulette/(?P<session_id>[0-9a-f-]+)/$', consumers.RouletteConsumer.as_asgi())

]
