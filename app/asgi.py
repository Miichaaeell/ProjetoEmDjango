"""
ASGI config for app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from boot.consumers import NotificationConsumer
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket':AllowedHostsOriginValidator(
                    AuthMiddlewareStack(
                        URLRouter(
                            path('/', NotificationConsumer.as_asgi()),
                            path('chat/', NotificationConsumer.as_asgi()),
                            path('conversa/<int:id_cliente>/', NotificationConsumer.as_asgi()),
                        )  
                )
            )
        }
    )
