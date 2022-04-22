from django.urls import re_path

from games.slots.web import consumers

websocket_urlpatterns = [
    re_path(r'ws/slots/(?P<session_id>[0-9a-f-]+)/$', consumers.SlotsConsumer.as_asgi())
]
