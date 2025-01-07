from django.urls import path

from . import views

urlpatterns = [
    # Manage user's courses (list view)
    path(
        'mine/',
        views.ManageCourseListView.as_view(),
        name='manage_course_list',
    ),

    # Create a new course
    path(
        'create/',
        views.CourseCreateView.as_view(),
        name='course_create',
    ),

    # Edit an existing course identified by its primary key (pk)
    path(
        '<pk>/edit/',
        views.CourseUpdateView.as_view(),
        name='course_edit',
    ),

    # Delete an existing course identified by its primary key (pk)
    path(
        '<pk>/delete/',
        views.CourseDeleteView.as_view(),
        name='course_delete',
    ),

    # Update course modules for a specific course identified by its primary key (pk)
    path(
        '<pk>/module/',
        views.CourseModuleUpdateView.as_view(),
        name='course_module_update',
    ),

    # Create new content for a specific module and content type (model_name)
    path(
        'module/<int:module_id>/content/<model_name>/create/',
        views.ContentCreateUpdateView.as_view(),
        name='module_content_create',
    ),

    # Update existing content for a specific module and content type (model_name)
    path(
        'module/<int:module_id>/content/<model_name>/<id>/',
        views.ContentCreateUpdateView.as_view(),
        name='module_content_update',
    ),

    # Delete specific content by its ID
    path(
        'content/<int:id>/delete/',
        views.ContentDeleteView.as_view(),
        name='module_content_delete',
    ),

    # List all contents in a specific module
    path(
        'module/<int:module_id>/',
        views.ModuleContentListView.as_view(),
        name='module_content_list',
    ),

    # Reorder modules for a course
    path(
        'module/order/',
        views.ModuleOrderView.as_view(),
        name='module_order',
    ),

    # Reorder content items within a module
    path(
        'content/order/',
        views.ContentOrderView.as_view(),
        name='content_order',
    ),

    # List courses filtered by a specific subject (slug)
    path(
        'subject/<slug:subject>/',
        views.CourseListView.as_view(),
        name='course_list_subject',
    ),

    # Display details for a specific course identified by its slug
    path(
        '<slug:slug>/',
        views.CourseDetailView.as_view(),
        name='course_detail',
    ),
]
