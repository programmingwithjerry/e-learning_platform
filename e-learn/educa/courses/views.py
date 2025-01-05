from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.apps import apps
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.core.cache import cache
from django.db.models import Count
from django.forms.models import modelform_factory
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from students.forms import CourseEnrollForm

from .forms import ModuleFormSet
from .models import Content, Course, Module, Subject

# Base mixins for ownership and edit permissions
class OwnerMixin:
    """
    Mixin to filter the queryset by the currently logged-in user (owner).
    """
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin:
    """
    Mixin to automatically assign the logged-in user as the owner of a form instance.
    """
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


# Mixins for managing courses with ownership and permissions
class OwnerCourseMixin(
    OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin
):
    """
    Mixin for views that manage courses owned by the logged-in user.
    """
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    """
    Mixin for views that edit courses owned by the logged-in user.
    """
    template_name = 'courses/manage/course/form.html'


# Views for managing courses
class ManageCourseListView(OwnerCourseMixin, ListView):
    """
    View to display the list of courses owned by the logged-in user.
    """
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    """
    View to create a new course.
    """
    permission_required = 'courses.add_course'


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    """
    View to update an existing course.
    """
    permission_required = 'courses.change_course'


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    """
    View to delete a course.
    """
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'


# Views for managing course modules
class CourseModuleUpdateView(TemplateResponseMixin, View):
    """
    View to manage a module formset for a course.
    """
    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        """Return the module formset."""
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        """Retrieve the course and validate ownership."""
        self.course = get_object_or_404(
            Course, id=pk, owner=request.user
        )
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        """Handle GET requests to render the formset."""
        formset = self.get_formset()
        return self.render_to_response(
            {'course': self.course, 'formset': formset}
        )

    def post(self, request, *args, **kwargs):
        """Handle POST requests to save the formset."""
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response(
            {'course': self.course, 'formset': formset}
        )


# Views for managing course content
class ContentCreateUpdateView(TemplateResponseMixin, View):
    """
    View to create or update course content.
    """
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        """Retrieve the model class based on the model name."""
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(
                app_label='courses', model_name=model_name
            )
        return None

    def get_form(self, model, *args, **kwargs):
        """Return a model form for the given model."""
        Form = modelform_factory(
            model, exclude=['owner', 'order', 'created', 'updated']
        )
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        """Retrieve the module and validate ownership."""
        self.module = get_object_or_404(
            Module, id=module_id, course__owner=request.user
        )
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(
                self.model, id=id, owner=request.user
            )
        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        """Handle GET requests to render the content form."""
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response(
            {'form': form, 'object': self.obj}
        )

    def post(self, request, module_id, model_name, id=None):
        """Handle POST requests to save content."""
        form = self.get_form(
            self.model,
            instance=self.obj,
            data=request.POST,
            files=request.FILES,
        )
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # New content
                Content.objects.create(module=self.module, item=obj)
            return redirect('module_content_list', self.module.id)
        return self.render_to_response(
            {'form': form, 'object': self.obj}
        )


class ContentDeleteView(View):
    """
    View to delete course content.
    """
    def post(self, request, id):
        """Handle POST requests to delete content."""
        content = get_object_or_404(
            Content, id=id, module__course__owner=request.user
        )
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module.id)


# Views for listing and ordering modules and contents
class ModuleContentListView(TemplateResponseMixin, View):
    """
    View to list all contents of a module.
    """
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        """Handle GET requests to render the content list."""
        module = get_object_or_404(
            Module, id=module_id, course__owner=request.user
        )
        return self.render_to_response({'module': module})


class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    """
    View to handle AJAX requests for reordering modules.
    """
    def post(self, request):
        """Handle POST requests to update module order."""
        for id, order in self.request_json.items():
            Module.objects.filter(
                id=id, course__owner=request.user
            ).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    """
    View to handle AJAX requests for reordering contents.
    """
    def post(self, request):
        """Handle POST requests to update content order."""
        for id, order in self.request_json.items():
            Content.objects.filter(
                id=id, module__course__owner=request.user
            ).update(order=order)
        return self.render_json_response({'saved': 'OK'})


# Views for displaying courses to students
class CourseListView(TemplateResponseMixin, View):
    """
    View to list courses based on the selected subject or show all courses.
    
    Attributes:
        model (Model): The Course model for querying course data.
        template_name (str): Template used to render the course list.
    """

    model = Course
    template_name = 'courses/course/list.html'

    def get(self, request, subject=None):
        """
        Handles GET requests to display courses and subjects.
        
        Caches subjects and courses for performance optimization. Filters 
        courses based on the selected subject if provided.
        
        Args:
            request (HttpRequest): The HTTP request object.
            subject (str, optional): Slug of the subject to filter courses.
        
        Returns:
            HttpResponse: Rendered template with subjects and courses context.
        """
        # Retrieve all subjects from the cache or query and cache them.
        subjects = cache.get('all_subjects')
        if not subjects:
            subjects = Subject.objects.annotate(
                total_courses=Count('courses')  # Add total courses count for each subject
            )
            cache.set('all_subjects', subjects)

        # Retrieve all courses and annotate with total modules.
        all_courses = Course.objects.annotate(
            total_modules=Count('modules')
        )

        if subject:
            # If a subject is selected, filter courses by subject.
            subject = get_object_or_404(Subject, slug=subject)
            key = f'subject_{subject.id}_courses'
            courses = cache.get(key)
            if not courses:
                courses = all_courses.filter(subject=subject)
                cache.set(key, courses)
        else:
            # If no subject is selected, retrieve all courses from cache or query.
            courses = cache.get('all_courses')
            if not courses:
                courses = all_courses
                cache.set('all_courses', courses)

        # Render the response with subjects, selected subject, and courses.
        return self.render_to_response(
            {
                'subjects': subjects,
                'subject': subject,
                'courses': courses,
            }
        )


class CourseDetailView(DetailView):
    """
    View to display detailed information about a specific course.
    Attributes:
        model (Model): The Course model for querying course data.
        template_name (str): Template used to render the course detail page.
    """

    model = Course
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs):
        """
        Add extra context to the template, including an enrollment form.

        Args:
            **kwargs: Additional context parameters.

        Returns:
            dict: Context dictionary with additional data.
        """
        # Call the parent class's method to get default context.
        context = super().get_context_data(**kwargs)

        # Add an enrollment form pre-filled with the course information.
        context['enroll_form'] = CourseEnrollForm(
            initial={'course': self.object}
        )

        return context
