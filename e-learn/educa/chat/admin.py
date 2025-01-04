from django.contrib import admin
from chat.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Admin interface customization for the Message model.
    Defines how Message objects are displayed, filtered, and searched in the Django admin panel.
    """

    # Specifies the fields to display in the list view of the admin panel
    list_display = ['sent_on', 'user', 'course', 'content']
    # - 'sent_on': Shows the timestamp of when the message was sent.
    # - 'user': Displays the user who sent the message.
    # - 'course': Displays the course the message is associated with.
    # - 'content': Displays the content of the message.

    # Adds filtering options in the admin panel
    list_filter = ['sent_on', 'course']
    # - 'sent_on': Enables filtering by the date/time the message was sent.
    # - 'course': Enables filtering by the associated course.

    # Adds a search bar in the admin panel to search messages
    search_fields = ['content']
    # - 'content': Allows searching through the message content.

    # Optimizes foreign key fields by using raw ID inputs instead of dropdowns
    raw_id_fields = ['user', 'content']
    # - 'user': Displays a raw ID field for selecting the user, useful when the user base is large.
    # - 'content': Displays a raw ID field for the content, though it may not be commonly needed here.
