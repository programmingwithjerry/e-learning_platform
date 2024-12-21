# Import the path function to define URL patterns
from django.urls import path

# Import the views module to reference view classes and functions
from . import views

# Define the URL patterns for the app
urlpatterns = [
    # URL pattern for the student registration view
    # When users navigate to 'register/', the StudentRegistrationView is displayed
    path(
        'register/',  # The URL path for registration
        views.StudentRegistrationView.as_view(),  # The view to handle the request
        name='student_registration'  # The name of the URL pattern for reverse lookups
    ),
]
