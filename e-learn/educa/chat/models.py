from django.conf import settings
from django.db import models

class Message(models.Model):
    """
    A model representing a chat message in a course's chat room.
    Stores information about the user who sent the message, the course it belongs to,
    the message content, and the time it was sent.
    """
    # The user who sent the message
    # Uses a foreign key to the user model specified in AUTH_USER_MODEL
    # Protects the message from being deleted if the user is deleted
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Reference to the user model
        on_delete=models.PROTECT,  # Prevent deletion if the user exists
        related_name='chat_messages'  # Allows reverse lookup from the user model
    )

    # The course to which the message belongs
    # Uses a foreign key to the Course model
    # Protects the message from being deleted if the course is deleted
    course = models.ForeignKey(
        'courses.Course',  # Reference to the Course model
        on_delete=models.PROTECT,  # Prevent deletion if the course exists
        related_name='chat_messages'  # Allows reverse lookup from the course model
    )

    # The content of the message
    content = models.TextField()

    # Timestamp when the message was sent
    # Automatically sets the value to the current date and time when the message is created
    sent_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the message.
        Includes the user's name, the course name, and the timestamp of the message.
        """
        return f'{self.user} on {self.course} at {self.sent_on}'
