"""
ASGI config for educa project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from django.core.asgi import get_asgi_application
from chat.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'educa.settings')

django_asgi_app = get_asgi_application()

# Define the ASGI application routing
application = ProtocolTypeRouter({
    # Route HTTP protocol to the default Django ASGI application
    'http': django_asgi_app,
    # Route WebSocket protocol to the WebSocket URL patterns
    'websocket': AuthMiddlewareStack(  # Wrap WebSocket connections with authentication middleware
        URLRouter(websocket_urlpatterns)  # Route WebSocket connections based on defined URL patterns
    ),
})
