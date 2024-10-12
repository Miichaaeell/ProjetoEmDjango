from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat-socket/', consumers.NotificationConsumer.as_asgi()),

]