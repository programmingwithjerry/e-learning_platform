"""
This module contains serializers for the Course, Module, Content, and Subject models.
The serializers are used to convert model instances into JSON format for use in APIs.
"""

from django.db.models import Count
from rest_framework import serializers

from courses.models import Content, Course, Module, Subject


class SubjectSerializer(serializers.ModelSerializer):
    """
    Serializer for the Subject model.
    Includes fields for basic subject details, total courses count, 
    and a list of the most popular courses in the subject.
    """
    total_courses = serializers.IntegerField()
    popular_courses = serializers.SerializerMethodField()

    def get_popular_courses(self, obj):
        """
        Retrieve the top 3 courses with the highest number of students in the subject.
        """
        courses = obj.courses.annotate(
            total_students=Count('students')
        ).order_by('-total_students')[:3]
        return [
            f'{c.title} ({c.total_students} students)' for c in courses
        ]

    class Meta:
        model = Subject
        fields = [
            'id',
            'title',
            'slug',
            'total_courses',
            'popular_courses',
        ]


class ModuleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Module model.
    Includes fields for module order, title, and description.
    """
    class Meta:
        model = Module
        fields = ['order', 'title', 'description']


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Course model.
    Includes fields for course details and associated modules.
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
            'modules',
        ]


class ItemRelatedField(serializers.RelatedField):
    """
    Custom RelatedField for rendering item content in Content model.
    """
    def to_representation(self, value):
        """
        Render the item's content using its render method.
        """
        return value.render()


class ContentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Content model.
    Includes fields for content order and the rendered item.
    """
    item = ItemRelatedField(read_only=True)

    class Meta:
        model = Content
        fields = ['order', 'item']


class ModuleWithContentsSerializer(serializers.ModelSerializer):
    """
    Serializer for the Module model with nested contents.
    """
    contents = ContentSerializer(many=True)

    class Meta:
        model = Module
        fields = ['order', 'title', 'description', 'contents']


class CourseWithContentsSerializer(serializers.ModelSerializer):
    """
    Serializer for the Course model with nested modules and contents.
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
            'modules',
        ]
