from django.db.models import Count
# Importing the necessary modules from Django REST Framework
from rest_framework import serializers
# Importing the Subject model from the courses app
from courses.models import Content, Course, Module, Subject

class ItemRelatedField(serializers.RelatedField):
    """
    Custom serializer field to render a related item.

    This custom `RelatedField` is used to render a related object in a specific format.
    In this case, the field calls the `render()` method of the related object to return
    a specific representation.

    Methods:
        to_representation: Converts the related object into a custom representation.
    """

    def to_representation(self, value):
        """
        Converts the related object to a custom representation.

        This method is used to return a specific representation of the related object. 
        In this case, it calls the `render()` method of the `value` (the related object).

        Args:
            value (object): The related object to be serialized.

        Returns:
            str: The custom representation of the related object as returned by the `render()` method.
        """
        return value.render()

class ContentSerializer(serializers.ModelSerializer):
    """
    Serializer for the `Content` model.

    This serializer is used to convert the `Content` model instances into JSON data
    that can be sent as a response. It includes a custom `ItemRelatedField` for the
    `item` field to control how related objects are represented.

    Fields:
        order (int): The order of the content.
        item (ItemRelatedField): The related item to be rendered in a custom format.
    """

    item = ItemRelatedField(read_only=True)

    class Meta:
        model = Content
        fields = ['order', 'item']


class ModuleWithContentsSerializer(serializers.ModelSerializer):
    """
    Serializer for the `Module` model with its associated `Contents`.

    This serializer is used to represent a `Module` instance along with its related `Contents`.
    The `contents` field is serialized using the `ContentSerializer` to provide a detailed representation
    of the associated content items for that module.

    Fields:
        order (int): The order of the module in the course.
        title (str): The title of the module.
        description (str): A description of the module.
        contents (List[ContentSerializer]): A list of content items related to the module, serialized with `ContentSerializer`.
    """

    contents = ContentSerializer(many=True)

    class Meta:
        model = Module
        fields = ['order', 'title', 'description', 'contents']


class CourseWithContentsSerializer(serializers.ModelSerializer):
    """
    Serializer for the `Course` model with its associated `Modules` and `Contents`.

    This serializer is used to represent a `Course` instance along with its related `Modules`.
    Each module is serialized using the `ModuleWithContentsSerializer`, which also includes the
    associated content items for that module.

    Fields:
        id (int): The unique identifier for the course.
        subject (SubjectSerializer): The subject associated with the course.
        title (str): The title of the course.
        slug (str): A URL-friendly identifier for the course.
        overview (str): A brief overview or description of the course.
        created (datetime): The creation date of the course.
        owner (UserSerializer): The owner (creator) of the course.
        modules (List[ModuleWithContentsSerializer]): A list of modules in the course, each serialized with `ModuleWithContentsSerializer`.
    """

    modules = ModuleWithContentsSerializer(many=True)

    class Meta:
        model = Course
        fields = [
            'id',
            'subject',
            'title',
            'slug',
            'overview',
            'created',
            'owner',
            'modules'
        ]


class ModuleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Module model.

    This serializer converts Module model instances to JSON format and vice versa.
    It is used to serialize the data when sending or receiving information about
    modules within a course through the API.

    The fields included in the serialized data are:
    - 'order': The position of the module within a course (used for ordering modules).
    - 'title': The title or name of the module.
    - 'description': A brief description of what the module covers.

    Attributes:
        model (class): The model to be serialized (Module).
        fields (list): The list of fields to include in the serialization process.
    """
    class Meta:
        model = Module
        fields = ['order', 'title', 'description']

# Creating a serializer for the Subject model
class SubjectSerializer(serializers.ModelSerializer):
    # Meta class is used to define the model and fields that should be serialized
    total_courses = serializers.IntegerField()
    popular_courses = serializers.SerializerMethodField()

    def get_popular_courses(self, obj):
        """
        Retrieves the top 3 most popular courses based on the number of students enrolled.
        This method queries the related courses for the given object (e.g., a Subject) and annotates each
        course with the total number of students enrolled. It then orders the courses by the total number
        of students in ascending order and returns a list of the top 3 courses, displaying their title
        along with the number of students enrolled.

        Args:
            obj: The object (such as a Subject) for which the popular courses are being retrieved.

        Return:
            List of strings: A list of the top 3 popular courses with their titles and student counts.
        """
        # Annotate courses with the number of students enrolled and order by total students
        courses = obj.courses.annotate(
            total_students=Count('students')
        ).order_by('total_students')[:3]
        # Return the list of popular courses with titles and student counts
        return [
            f'{c.title} ({c.total_students})' for c in courses
        ]

    class Meta:
        # Specify the model that this serializer will work with
        model = Subject
        # List the fields that should be included in the serialized output
        fields = ['id', 'title', 'slug', 'total_courses', 'popular_courses']


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Course model.

    This serializer converts Course model instances to JSON format and vice versa.
    It is used to serialize the data when sending or receiving information about
    courses through the API.

    The fields included in the serialized data are:
    - 'id': The unique identifier for the course.
    - 'subject': The subject to which the course belongs.
    - 'title': The title of the course.
    - 'slug': A URL-friendly version of the title, often used in URLs.
    - 'overview': A brief description of the course.
    - 'created': The date and time when the course was created.
    - 'owner': The user who owns or created the course.
    - 'modules': The list of modules or sections within the course.

    Attributes:
        model (class): The model to be serialized (Course).
        fields (list): The list of fields to include in the serialization process.
    """
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id',
            'subject',
            'title',
            'slug',
            'overview',
            'created',
            'owner',
            'modules'
        ]
