from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    # Route for student registration
    path(
        'register/',
        views.StudentRegistrationView.as_view(),
        name='student_registration',
    ),

    # Route for students to enroll in a course
    path(
        'enroll-course/',
        views.StudentEnrollCourseView.as_view(),
        name='student_enroll_course',
    ),

    # Route to display the list of courses a student is enrolled in
    path(
        'courses/',
        views.StudentCourseListView.as_view(),
        name='student_course_list',
    ),

    # Route to display detailed information about a specific course
    # Caches the view for 15 minutes to improve performance
    path(
        'course/<pk>/',
        cache_page(60 * 15)(views.StudentCourseDetailView.as_view()),
        name='student_course_detail',
    ),

    # Route to display a specific module within a course
    # Caches the view for 15 minutes to improve performance
    path(
        'course/<pk>/<module_id>/',
        cache_page(60 * 15)(views.StudentCourseDetailView.as_view()),
        name='student_course_detail_module',
    ),
]
