from django.urls import path  # Import the path function to define URL patterns
from . import views  # Import views from the current application

# Define the namespace for this set of URLs, useful for referencing in templates or other parts of the app
app_name = 'chat'

# List of URL patterns for the chat application
urlpatterns = [
    # Define a URL pattern for the course chat room
    path(
        'room/<int:course_id>/',  # The URL pattern with a dynamic segment for the course ID
        views.course_chat_room,  # The view function to handle this URL
        name='course_chat_room'  # Name for this URL pattern, used for reverse resolution
    ),
]
