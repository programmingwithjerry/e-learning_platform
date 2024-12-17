from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateResponseMixin, View
from .forms import ModuleFormSet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from .models import Course
from django.contrib.auth.mixins import (
	LoginRequiredMixin,
	PermissionRequiredMixin
)


# Define the view for managing the list of courses, inheriting from ListView
class ManageCourseListView(ListView):
    # Specify the model to use for this view (Course model)
    model = Course
    # Define the template to render for this view
    template_name = 'courses/manage/course/list.html'

    #Override the get_queryset method to filter courses by thelogged-in user
    def get_queryset(self):
        # Get the base queryset from the ListView
        qs = super().get_queryset()
        #Filter the queryset to only include courses owned by thecurrent user
        return qs.filter(owner=self.request.user)


# Mixin class that provides owner filtering for queryset
class OwnerMixin:
    # Method to return the queryset filtered by the current user's ownership
    def get_queryset(self):
        # Get the base queryset from the parent class
        qs = super().get_queryset()
        # Filter the queryset to include only objects owned by the current user
        return qs.filter(owner=self.request.user)

# Mixin class that sets the owner field on form submission
class OwnerEditMixin:
    # Method called when the form is valid, setting the owner before saving
    def form_valid(self, form):
        # Set the owner of the form instance to the current logged-in user
        form.instance.owner = self.request.user
        # Call the parent form_valid method to complete the form submission
        return super().form_valid(form)

# Mixin class combining ownership filtering and other required mixins
class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    # Define the model to use in this mixin (Course model)
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    # Define the success URL to redirect to after a successful action
    success_url = reverse_lazy('manage_course_list')

class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    # Specify the template to use for the course form
    template_name = 'courses/manage/course/form.html'

# View for managing the list of courses
class ManageCourseListView(OwnerCourseMixin, ListView):
    # Define the template to render for the course list view
    template_name = 'courses/manage/course/list.html'
    # Specify the permission required to view the courses
    permission_required = 'courses.view_course'

# View for creating a new course
class CourseCreateView(OwnerCourseEditMixin, CreateView):
    # Specify the permission required to create a new course
    permission_required = 'courses.add_course'

# View for updating an existing course
class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    # Specify the permission required to update a course
    permission_required = 'courses.change_course'

# View for deleting a course, inheriting from OwnerCourseMixin and DeleteView
class CourseDeleteView(OwnerCourseMixin, DeleteView):
    # Define the template to use for the course delete confirmation
    template_name = 'courses/manage/course/delete.html'
    # Specify the permission required to delete a course
    permission_required = 'courses.delete_course'

"""View for updating the course modules, inheriting
   from TemplateResponseMixin and View"""
class CourseModuleUpdateView(TemplateResponseMixin, View):
    # Define the template to use for the course module formset
    template_name = 'courses/manage/module/formset.html'
    # Initialize the course to None; it will be set in dispatch
    course = None

    # Method to return the formset for modules related to the course
    def get_formset(self, data=None):
        # Return a formset instance for the given course, with optional data
        return ModuleFormSet(instance=self.course, data=data)

    # Method to handle the dispatch of the request, setting the course object
    def dispatch(self, request, pk):
        """Get the course object based on the provided ID and
           ensure it belongs to the logged-in user"""
        self.course = get_object_or_404(
            Course, id=pk, owner=request.user
        )
        # Call the parent dispatch method to proceed with the request
        return super().dispatch(request, pk)

    # GET method for rendering the formset on the page
    def get(self, request, *args, **kwargs):
        # Get the formset for the course
        formset = self.get_formset()
        # Render the template with the course and formset data
        return self.render_to_response(
            {'course': self.course, 'formset': formset}
        )

    # POST method to handle the submitted formset data
    def post(self, request, *args, **kwargs):
        # Get the formset with the submitted data
        formset = self.get_formset(data=request.POST)
        # Check if the formset is valid
        if formset.is_valid():
            # Save the formset data to the database
            formset.save()
            # Redirect to the manage course list page upon success
            return redirect('manage_course_list')
        # If the formset is not valid, re-render the formset with errors
        return self.render_to_response(
            {'course': self.course, 'formset': formset}
        )
