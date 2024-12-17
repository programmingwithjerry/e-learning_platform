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

# Importing settings from Django configuration
from django.conf import settings
# Importing static file handling for development
from django.conf.urls.static import static
# Importing Django's admin module to manage the admin interface
from django.contrib import admin
# Importing authentication views for login and logout functionality
from django.contrib.auth import views as auth_views
# Importing functions to handle URL routing
from django.urls import include, path

# Define URL patterns for the project
urlpatterns = [
    # Path for login page using Django's LoginView
    path(
        'accounts/login/', auth_views.LoginView.as_view(), name='login'
    ),
    """path(  # This path is commented out (Logout view)
        'accounts/logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),"""
    # Path for admin interface
    path('admin/', admin.site.urls),
    # Path for course URLs handled by the 'courses' app
    path('course/', include('courses.urls')),
]

# Add static file handling in development mode
if settings.DEBUG:
    # Serve media files in development mode
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
