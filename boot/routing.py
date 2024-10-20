from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path(r'ws/chat-socket/', consumers.NotificationConsumer.as_asgi()),

]