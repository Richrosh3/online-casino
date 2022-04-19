from django.urls import re_path

from games.craps.web import consumers


websocket_urlpatterns = [
    re_path(r'ws/craps/(?P<session_id>[0-9a-f-]+)/$', consumers.CrapsConsumer.as_asgi())
]
