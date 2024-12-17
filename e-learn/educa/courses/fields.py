# Importing exception to handle when no object is found
from django.core.exceptions import ObjectDoesNotExist
# Importing models for database field definitions
from django.db import models

# Custom field class inheriting from PositiveIntegerField
class OrderField(models.PositiveIntegerField):
    # Constructor accepting optional fields for filtering
    def __init__(self, for_fields=None, *args, **kwargs):
        # Store the fields to filter by
        self.for_fields = for_fields
        # Call parent constructor with any remaining arguments
        super().__init__(*args, **kwargs)

    # Overriding pre_save method to handle value assignment
    def pre_save(self, model_instance, add):
        # Check if the field value is not set
        if getattr(model_instance, self.attname) is None:
            # No current value assigned to this field
            try:
                # Get all objects of the model
                qs = self.model.objects.all()
                # Check if there are fields to filter by
                if self.for_fields:
                    # Dynamically generate filter conditions
                    query = {
                        # For each field in "for_fields", add it to the filter
                        field: getattr(model_instance, field)
                        for field in self.for_fields
                    }
                    # Apply filter conditions to queryset
                    qs = qs.filter(**query)
                # Retrieve the last item based on the order field
                last_item = qs.latest(self.attname)
                # Set the new order value as one more than the last item
                value = getattr(last_item, self.attname) + 1
            except ObjectDoesNotExist:  # Handle case where no objects are found
                # Default to 0 if no previous items exist
                value = 0
            # Assign the calculated value to the field
            setattr(model_instance, self.attname, value)
            # Return the new value for the field
            return value
        else:
            # Call the parent's pre_save if value is already set
            return super().pre_save(model_instance, add)
