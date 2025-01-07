from courses.models import Course
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView

from .forms import CourseEnrollForm


class StudentRegistrationView(CreateView):
    """
    View for student registration using Django's built-in UserCreationForm.
    Upon successful registration, the user is logged in and redirected
    to their course list.
    """
    template_name = 'students/student/registration.html'  # Template for registration
    form_class = UserCreationForm  # Form class for user creation
    success_url = reverse_lazy('student_course_list')  # Redirect on successful registration

    def form_valid(self, form):
        """
        Process the valid form, authenticate the user, and log them in.
        """
        result = super().form_valid(form)
        cd = form.cleaned_data
        # Authenticate the user using the provided username and password
        user = authenticate(username=cd['username'], password=cd['password1'])
        # Log the user in
        login(self.request, user)
        return result


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    """
    View to handle course enrollment for students.
    Requires the user to be logged in.
    """
    course = None  # Placeholder for the course to be enrolled
    form_class = CourseEnrollForm  # Form class for course enrollment

    def form_valid(self, form):
        """
        Enroll the logged-in user in the selected course.
        """
        self.course = form.cleaned_data['course']
        # Add the current user to the course's student list
        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        """
        Redirect the user to the course detail page after enrollment.
        """
        return reverse_lazy('student_course_detail', args=[self.course.id])


class StudentCourseListView(LoginRequiredMixin, ListView):
    """
    View to display the list of courses the logged-in student is enrolled in.
    """
    model = Course  # The model to query
    template_name = 'students/course/list.html'  # Template for course list

    def get_queryset(self):
        """
        Filter courses to only include those the logged-in user is enrolled in.
        """
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])


class StudentCourseDetailView(LoginRequiredMixin, DetailView):
    """
    View to display details of a specific course the logged-in student is enrolled in.
    Includes the course modules and highlights the selected module.
    """
    model = Course  # The model to query
    template_name = 'students/course/detail.html'  # Template for course detail

    def get_queryset(self):
        """
        Filter courses to only include those the logged-in user is enrolled in.
        """
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        """
        Add additional context to the course detail page, including
        the selected module or the first module by default.
        """
        context = super().get_context_data(**kwargs)
        course = self.get_object()  # Get the current course object
        if 'module_id' in self.kwargs:
            # If module_id is in the URL, get the specified module
            context['module'] = course.modules.get(id=self.kwargs['module_id'])
        else:
            # Otherwise, get the first module in the course
            context['module'] = course.modules.all()[0]
        return context
