from django.urls import include, path
from rest_framework import routers
from . import views

# Set the app namespace for URL namespacing in the Django project
app_name = 'courses'

router = routers.DefaultRouter()
router.register('courses', views.CourseViewSet)
router.register('subjects', views.SubjectViewSet)

# Define the URL patterns for the 'courses' app
urlpatterns = [
    # URL pattern for listing all subjects, maps to the SubjectListView
   # path(
    #    'subjects/',  # URL endpoint for the list of subjects
     #   views.SubjectListView.as_view(),  # Link this URL to the SubjectListView class
      #  name='subject_list'  # Name the URL for easy reference in templates and views
   # ),
    # URL pattern for retrieving a specific subject by primary key (pk), maps to the SubjectDetailView
   # path(
    #    'subjects/<pk>/',  # URL endpoint for viewing a specific subject by its primary key
     #   views.SubjectDetailView.as_view(),  # Link this URL to the SubjectDetailView class
      #  name='subject_detail'  # Name the URL for easy reference in templates and views
   # ),
#    path('', include(router.urls)),
#
 #   path(
  #      'courses/<pk>/enroll/',
   #     views.CourseEnrollView.as_view(),
    #    name='course_enroll'
#    ),
    path('', include(router.urls)),
]
