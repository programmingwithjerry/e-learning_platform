from django.contrib import admin

from chat.models import Message

# Register the Message model with the admin site
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Admin interface for the Message model.
    """

    # Fields to display in the admin list view
    list_display = ['sent_on', 'user', 'course', 'content']

    # Fields to filter messages in the admin interface
    list_filter = ['sent_on', 'course']

    # Fields to enable search functionality in the admin interface
    search_fields = ['content']

    # Fields to display as raw ID widgets for optimized selection
    raw_id_fields = ['user', 'course']
