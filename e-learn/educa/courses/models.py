"""from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from .fields import OrderField
from django.db import models"""


# Import the necessary models module from Django
from django.db import models
from django.contrib.auth.models import User

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


"""class Content(models.Model):
	module = models.ForeignKey(
		Module,
		related_name='contents',
		on_delete=models.CASCADE,
	)
	content_type = models.ForeignKey(
		ContentType,
		on_delete=models.CASCADE,
		limit_choices_to={
			'model__in':('text', 'video', 'image', 'file')
		}
	)
	object_id = models.PositiveIntegerField()
	item = GenericForeignKey('content_type', 'object_id')
	order = OrderField(blank=True, for_fields=['module'])

	class Meta:
		ordering = ['order']


class ItemBase(models.Model):
	owner = models.ForeignKey(User,
		related_name='%(class)s_related',
		on_delete=models.CASCADE
	)
	title = models.CharField(max_length=250)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True

	def __str__(self):
		return self.title


class Text(ItemBase):
	content = models.TextField()


class File(ItemBase):
	file = models.FileField(upload_to='files')


class Image(ItemBase):
	file = models.FileField(upload_to='images')


class Video(ItemBase):
	url = models.URLField()"""
