from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.loader import render_to_string

from .fields import OrderField


class Subject(models.Model):
    """
    Model representing a subject or category for courses.
    """

    title = models.CharField(max_length=200)  # Title of the subject
    slug = models.SlugField(max_length=200, unique=True)  # Unique identifier for the subject in URLs

    class Meta:
        ordering = ['title']  # Orders subjects alphabetically by title

    def __str__(self):
        return self.title


class Course(models.Model):
    """
    Model representing a course with details about its owner, subject, and enrolled students.
    """

    owner = models.ForeignKey(
        User, related_name='courses_created', on_delete=models.CASCADE
    )  # User who created the course
    subject = models.ForeignKey(
        Subject, related_name='courses', on_delete=models.CASCADE
    )  # The subject this course belongs to
    title = models.CharField(max_length=200)  # Title of the course
    slug = models.SlugField(max_length=200, unique=True)  # Unique identifier for the course in URLs
    overview = models.TextField()  # Overview or description of the course
    created = models.DateTimeField(auto_now_add=True)  # Timestamp for when the course was created
    students = models.ManyToManyField(
        User, related_name='courses_joined', blank=True
    )  # Students enrolled in the course

    class Meta:
        ordering = ['-created']  # Orders courses by newest first

    def __str__(self):
        return self.title


class Module(models.Model):
    """
    Model representing a module within a course.
    """

    course = models.ForeignKey(
        Course, related_name='modules', on_delete=models.CASCADE
    )  # The course this module belongs to
    title = models.CharField(max_length=200)  # Title of the module
    description = models.TextField(blank=True)  # Optional description of the module
    order = OrderField(blank=True, for_fields=['course'])  # Custom order field within the course

    class Meta:
        ordering = ['order']  # Orders modules by their specified order

    def __str__(self):
        return f'{self.order}. {self.title}'


class Content(models.Model):
    """
    Model representing an item of content in a module, which could be text, video, image, or file.
    """

    module = models.ForeignKey(
        Module, related_name='contents', on_delete=models.CASCADE
    )  # The module this content belongs to
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            'model__in': ('text', 'video', 'image', 'file')
        },
    )  # The type of content (text, video, image, file)
    object_id = models.PositiveIntegerField()  # ID of the related content object
    item = GenericForeignKey('content_type', 'object_id')  # Generic relation to the content object
    order = OrderField(blank=True, for_fields=['module'])  # Custom order field within the module

    class Meta:
        ordering = ['order']  # Orders content by their specified order


class ItemBase(models.Model):
    """
    Abstract base class for different types of content items (e.g., Text, File, Image, Video).
    """

    owner = models.ForeignKey(
        User, related_name='%(class)s_related', on_delete=models.CASCADE
    )  # User who created the content item
    title = models.CharField(max_length=250)  # Title of the content item
    created = models.DateTimeField(auto_now_add=True)  # Timestamp for when the item was created
    updated = models.DateTimeField(auto_now=True)  # Timestamp for when the item was last updated

    class Meta:
        abstract = True  # Specifies that this is an abstract base class

    def __str__(self):
        return self.title

    def render(self):
        """
        Renders the content item using a template specific to its type.
        """
        return render_to_string(
            f'courses/content/{self._meta.model_name}.html',
            {'item': self},
        )


# Concrete implementations of content items
class Text(ItemBase):
    """
    Model representing a text content item.
    """
    content = models.TextField()  # Text content


class File(ItemBase):
    """
    Model representing a file content item.
    """
    file = models.FileField(upload_to='files')  # Uploaded file path


class Image(ItemBase):
    """
    Model representing an image content item.
    """
    file = models.FileField(upload_to='images')  # Uploaded image path


class Video(ItemBase):
    """
    Model representing a video content item.
    """
    url = models.URLField()  # URL of the video
