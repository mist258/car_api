"""
ASGI config for configs project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings')

asgi = get_asgi_application()
from core.middlewares.auth_socket_middleware import AuthSocketMiddleware

from .routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'http': asgi,
    'websocket': AuthSocketMiddleware(URLRouter(websocket_urlpatterns)),
})
