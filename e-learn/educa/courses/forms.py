# Import the inlineformset_factory to create a formset for related models
from django.forms.models import inlineformset_factory  
# Import the Course and Module models to use in the formset
from .models import Course, Module  

# Create a formset for the Module model related to the Course model
ModuleFormSet = inlineformset_factory(  
    Course,  # The parent model
    Module,  # The related model
    fields=['title', 'description'],  # Fields to include in the formset
    extra=2,  # Number of extra blank forms to display
    can_delete=True  # Allow deletion of related Module instances
)
