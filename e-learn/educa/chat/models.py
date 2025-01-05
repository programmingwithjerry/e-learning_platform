from django.conf import settings
from django.db import models

class Message(models.Model):
    """
    Represents a chat message sent by a user in a specific course.
    Stores information about the sender, recipient course, message content,
    and timestamp when the message was sent.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Links to the user model
        on_delete=models.PROTECT,  # Prevent deletion of user if messages exist
        related_name='chat_messages',  # Related name for reverse lookup
    )
    course = models.ForeignKey(
        'courses.Course',  # Links to the Course model
        on_delete=models.PROTECT,  # Prevent deletion of course if messages exist
        related_name='chat_messages',  # Related name for reverse lookup
    )
    content = models.TextField()  # Field to store the content of the message
    sent_on = models.DateTimeField(auto_now_add=True)  # Timestamp when the message was sent

    def __str__(self):
        """
        Return a string representation of the message including the user,
        the course, and the timestamp when the message was sent.
        """
        return f'{self.user} on {self.course} at {self.sent_on}'
