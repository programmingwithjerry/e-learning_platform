# Import the path function to define URL patterns
from django.urls import path
# Import views from the current app to associate with the URL patterns
from . import views

# Define the URL patterns for the app
urlpatterns = [
    # URL pattern for managing the list of courses
    path(
        'mine/',  # URL segment for this view
        views.ManageCourseListView.as_view(),  # View to handle the request
        name='manage_course_list'  # Name of the URL pattern
    ),
    # URL pattern for creating a new course
    path(
        'create/',  # URL segment for this view
        views.CourseCreateView.as_view(),  # View to handle the request
        name='course_create'  # Name of the URL pattern
    ),
    # URL pattern for editing an existing course
    path(
        '<pk>/edit/',  # URL segment with a placeholder for the primary key
        views.CourseUpdateView.as_view(),  # View to handle the request
        name='course_edit'  # Name of the URL pattern
    ),
    # URL pattern for deleting an existing course
    path(
        '<pk>/delete/',  #URL segment with a placeholder for the primary key
        views.CourseDeleteView.as_view(),  # View to handle the request
        name='course_delete'  # Name of the URL pattern
    ),
    # URL pattern for updating course modules
    path(
        '<pk>/module/',  #URL segment with a placeholder for the primary key
        views.CourseModuleUpdateView.as_view(),  #View to handle the request
        name='course_module_update'  # Name of the URL pattern
    ),
]
