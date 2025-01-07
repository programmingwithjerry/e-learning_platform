"""
URL configuration for educa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from courses.views import CourseListView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

# Defining the main urlpatterns for the project
urlpatterns = [
    # User authentication: Login page
    path(
        'accounts/login/', auth_views.LoginView.as_view(), name='login'
    ),
    # User authentication: Logout page
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(),
        name='logout',
    ),
    # Admin site for managing the database and models
    path('admin/', admin.site.urls),
    # Including URL patterns for the courses app
    path('course/', include('courses.urls')),
    # Homepage: Displays a list of courses using the CourseListView
    path('', CourseListView.as_view(), name='course_list'),
    # Including URL patterns for the students app
    path('students/', include('students.urls')),
    # Including API-related URL patterns for the courses app
    path('api/', include('courses.api.urls', namespace='api')),
    # Including URL patterns for the chat functionality
    path('chat/', include('chat.urls', namespace='chat')),
    # Debug toolbar for development debugging
    path('__debug__/', include('debug_toolbar.urls')),
]

# If the DEBUG setting is True (development mode)
if settings.DEBUG:
    # Serve media files during development
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
