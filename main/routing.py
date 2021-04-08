# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/tictactoe/(?P<room_name>\w+)/(?P<unique_id>\w+)/$', consumers.TicTacToeConsumer.as_asgi()),
    re_path(r'ws/me/(?P<unique_id>\w+)/$', consumers.UserConsumer.as_asgi()),
]