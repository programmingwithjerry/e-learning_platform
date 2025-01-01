from django.urls import re_path  # Import re_path for defining URL patterns with regular expressions
from . import consumers  # Import consumers module from the current application

# Define the WebSocket URL patterns for the application
websocket_urlpatterns = [
    # Match WebSocket connections to the chat room endpoint
    re_path(
        r'ws/chat/room/(?P<course_id>\d+)/$',  # Regular expression for matching URLs with a course ID
        consumers.ChatConsumer.as_asgi()  # Use the ChatConsumer in ASGI-compatible form
    ),
]
