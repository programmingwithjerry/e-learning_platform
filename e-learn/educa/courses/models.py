# Import the necessary models module from Django
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
#from .fields import OrderField
from django.db import models

# Subject model represents the subject categories for courses
class Subject(models.Model):
    # Title of the subject with a max length of 200 characters
    title = models.CharField(max_length=200)
    # Unique slug for the subject, used in URLs
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        # Order subjects alphabetically by their title
        ordering = ['title']

    def __str__(self):
        # String representation of the subject
        return self.title


# Course model represents individual courses under specific subjects
class Course(models.Model):
    # User who created the course (owner), linked via ForeignKey
    owner = models.ForeignKey(
        User,  # Reference to Django's built-in User model
        related_name='courses_created',  # Reverse relationship name
        on_delete=models.CASCADE  # Delete courses if the user is deleted
    )
    # Subject under which the course falls
    subject = models.ForeignKey(
        Subject,  # Reference to the Subject model
        related_name='courses',  # Reverse relationship name
        on_delete=models.CASCADE #Delete courses if the subject is deleted
    )
    # Title of the course with a max length of 200 characters
    title = models.CharField(max_length=200)
    # Unique slug for the course, used in URLs
    slug = models.SlugField(max_length=200, unique=True)
    # Detailed overview/description of the course
    overview = models.TextField()
    # Timestamp for when the course is created, auto-set on creation
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Order courses by creation date, most recent first
        ordering = ['-created']

    def __str__(self):
        # String representation of the course
        return self.title


# Module model represents a unit or section within a specific course
class Module(models.Model):
    # ForeignKey linking the module to its parent course
    course = models.ForeignKey(
        Course,  # Reference to the Course model
        related_name='modules',  # Reverse relationship name
        on_delete=models.CASCADE  # Delete modules if the course is deleted
    )
    # Title of the module with a max length of 200 characters
    title = models.CharField(max_length=200)
    # Optional description field for the module
    description = models.TextField(blank=True)
    # Order field to determine the module's position within the course
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        # Order modules based on the 'order' field
        ordering = ['order']

    def __str__(self):
        # String representation of the module showing its order and title
        return f'{self.order}. {self.title}'


"""Content model represents generic content items
   (text, video, image, file) within a module
"""
class Content(models.Model):
    # ForeignKey linking the content to a specific module
    module = models.ForeignKey(
        Module,  # Reference to the Module model
        related_name='contents',  # Reverse relationship name
        on_delete=models.CASCADE  # Delete content if the module is deleted
    )
    # ForeignKey to the ContentType model for generic relationships
    content_type = models.ForeignKey(
        ContentType,  # Reference to Django's ContentType framework
        on_delete=models.CASCADE, #Delete content ifthe ContentType isdeleted
        limit_choices_to={  # Restrict choices to specific models
            'model__in': ('text', 'video', 'image', 'file')
        }
    )
    # PositiveIntegerField to store the ID of the related object
    object_id = models.PositiveIntegerField()
    """GenericForeignKey to create a relationship to
       any model specified in content_type
    """
    item = GenericForeignKey('content_type', 'object_id')
    # Custom order field to define the order of content within a module
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        # Order content items by the 'order' field within a module
        ordering = ['order']


# Base model to define common fields for content types
class ItemBase(models.Model):
    # ForeignKey linking the item to its owner (user)
    owner = models.ForeignKey(
        User,  # Reference to Django's built-in User model
        related_name='%(class)s_related',
        on_delete=models.CASCADE  # Delete the item if the user is deleted
    )
    # Title of the item with a max length of 250 characters
    title = models.CharField(max_length=250)
    # Timestamp for when the item is created; auto-set on creation
    created = models.DateTimeField(auto_now_add=True)
    # Timestamp for when the item is last updated; auto-updated on save
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        # Mark this model as abstract; it won't create a database table
        abstract = True

    def __str__(self):
        # String representation of the item
        return self.title


# Model for text-based content
class Text(ItemBase):
    # Field to store the text content
    content = models.TextField()


# Model for file-based content
class File(ItemBase):
    # Field to store uploaded files; files are saved in the 'files' directory
    file = models.FileField(upload_to='files')


# Model for image-based content
class Image(ItemBase):
    # Field to store uploaded images;images are saved in the'images'directory
    file = models.FileField(upload_to='images')


# Model for video-based content
class Video(ItemBase):
    # Field to store video URLs
    url = models.URLField()
