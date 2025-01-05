"""
This module defines viewsets for handling Subject and Course models in the API.
The viewsets provide endpoints for listing, retrieving, and performing actions on these models.
"""

from django.db.models import Count
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from courses.api.pagination import StandardPagination
from courses.api.permissions import IsEnrolled
from courses.api.serializers import (
    CourseSerializer,
    CourseWithContentsSerializer,
    SubjectSerializer,
)
from courses.models import Course, Subject


class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing and listing subjects.
    Subjects are annotated with the total number of courses.
    """
    queryset = Subject.objects.annotate(total_courses=Count('courses'))
    serializer_class = SubjectSerializer
    pagination_class = StandardPagination


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing and listing courses.
    Supports actions for enrolling users and retrieving course contents.
    """
    queryset = Course.objects.prefetch_related('modules')
    serializer_class = CourseSerializer
    pagination_class = StandardPagination

    @action(
        detail=True,
        methods=['post'],
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated],
    )
    def enroll(self, request, *args, **kwargs):
        """
        Custom action for enrolling the authenticated user in a course.
        Adds the user to the course's students list.
        """
        course = self.get_object()
        course.students.add(request.user)
        return Response({'enrolled': True})

    @action(
        detail=True,
        methods=['get'],
        serializer_class=CourseWithContentsSerializer,
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated, IsEnrolled],
    )
    def contents(self, request, *args, **kwargs):
        """
        Custom action for retrieving the detailed contents of a course.
        Includes modules and their respective contents.
        """
        return self.retrieve(request, *args, **kwargs)
