from django import forms
from courses.models import Course


class CourseEnrollForm(forms.Form):
    """
    Form for enrolling a user in a course.
    """

    course = forms.ModelChoiceField(
        queryset=Course.objects.none(),
        widget=forms.HiddenInput
    )

    def __init__(self, *args, **kwargs):
        """
        Initializes the form and dynamically sets the queryset for the 'course' field.

        Args:
            *args: Variable-length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super(CourseEnrollForm, self).__init__(*args, **kwargs)
        # Populate the 'course' field with all available courses.
        self.fields['course'].queryset = Course.objects.all()
