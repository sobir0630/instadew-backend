from django.urls import re_path
from chat.consumers import ChatConsumer, PresenceConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/presence/', PresenceConsumer.as_asgi()),
]