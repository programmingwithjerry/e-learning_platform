from django.shortcuts import render
# Import the authenticate and login functions for handling user authentication
from django.contrib.auth import authenticate, login

# Import the built-in user creation form for registering new users
from django.contrib.auth.forms import UserCreationForm

# Import reverse_lazy to lazily evaluate URL reversals
from django.urls import reverse_lazy

# Import the CreateView class for creating views that handle form submissions
from django.views.generic.edit import CreateView

# Define a view for student registration
class StudentRegistrationView(CreateView):
    # Specify the template to be used for rendering the registration form
    template_name = 'students/student/registration.html'

    # Use the built-in user creation form for handling user registration
    form_class = UserCreationForm

    # Define the URL to redirect to upon successful form submission
    success_url = reverse_lazy('student_course_list')

    # Handle the form submission when it is valid
    def form_valid(self, form):
        # Call the parent class's form_valid method to save the form
        result = super().form_valid(form)

        # Get the cleaned data from the form
        cd = form.cleaned_data

        # Authenticate the user using the provided username and password
        user = authenticate(
            username=cd['username'], password=cd['password1']
        )

        # Log the authenticated user into the current session
        login(self.request, user)

        # Return the result of the parent class's form_valid method
        return result
