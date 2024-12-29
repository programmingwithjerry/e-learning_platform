from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from courses.models import Course, Subject
from courses.api.pagination import StandardPagination
from courses.api.serializers import CourseSerializer, SubjectSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing a list of courses or retrieving a specific course.

    This viewset provides the standard `list` and `retrieve` actions for the `Course` model.
    It supports reading the course details via API endpoints, with optional pagination.

    The viewset uses the following:
    - `queryset`: The queryset retrieves all courses, with related `modules` pre-fetched to optimize database queries.
    - `serializer_class`: The `CourseSerializer` is used to serialize the `Course` data.
    - `pagination_class`: The `StandardPagination` is applied to paginate the course list and control the number of items per page.

    Attributes:
        queryset (QuerySet): The list of courses to be displayed, with modules pre-fetched.
        serializer_class (class): The serializer used to convert course data into JSON format.
        pagination_class (class): The pagination class used to control the pagination of course data.
    """
    queryset = Course.objects.prefetch_related('modules')  # Prefetch related modules to optimize queries
    serializer_class = CourseSerializer  # Use CourseSerializer for serializing course data
    pagination_class = StandardPagination  # Apply pagination to the course list

    @action(
        detail=True,
        methods=['post'],
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated]
    )
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        course.students.add(request.user)
        return Response({'enrolled': True})

# View to list all Subject objects using a GET request
# class SubjectListView(generics.ListAPIView):
#     # Define the queryset for this view to fetch all Subject instances from the database
#     queryset = Subject.objects.annotate(total_courses=Count('courses'))
    # Specify the serializer to be used for converting Subject objects to JSON
    #serializer_class = SubjectSerializer
    #pagination_class = StandardPagination


# View to retrieve a single Subject object by its primary key (ID)
#class SubjectDetailView(generics.RetrieveAPIView):
    # Define the queryset for this view to fetch all Subject instances from the database
 #   queryset = Subject.objects.annotate(total_courses=Count('courses'))

    # Specify the serializer to be used for converting the Subject object to JSON
  #  serializer_class = SubjectSerializer


class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing a list of subjects or retrieving a specific subject.

    This viewset provides the standard `list` and `retrieve` actions for the `Subject` model.
    It supports reading the subject details through API endpoints, with optional pagination.
    Additionally, it annotates each subject with the total number of associated courses.

    The viewset uses the following:
    - `queryset`: The queryset retrieves all subjects, annotated with the count of courses (`total_courses`).
    - `serializer_class`: The `SubjectSerializer` is used to serialize the subject data.
    - `pagination_class`: The `StandardPagination` is applied to paginate the subject list and control the number of items per page.

    Attributes:
        queryset (QuerySet): The list of subjects to be displayed, with an annotation for the total number of courses.
        serializer_class (class): The serializer used to convert subject data into JSON format.
        pagination_class (class): The pagination class used to control the pagination of subject data.
    """
    queryset = Subject.objects.annotate(total_courses=Count('courses'))  # Annotate subjects with course count
    serializer_class = SubjectSerializer  # Use SubjectSerializer for serializing subject data
    pagination_class = StandardPagination  # Apply pagination to the subject list


#class CourseEnrollView(APIView):
    """
    A view for enrolling a user in a course.

    This view handles the enrollment of a user in a course by adding the user to the
    course's `students` field (a many-to-many relationship). It is a `POST` request that
    enrolls the authenticated user in the specified course.

    The course is identified by the `pk` (primary key) in the URL. If the course exists,
    the user making the request will be enrolled as a student in that course.

    Attributes:
        request (HttpRequest): The HTTP request object containing the user and course information.
        pk (int): The primary key of the course to enroll the user in.
        format (str, optional): The format for the response (usually not necessary).
    """
 #   authentication_classes = [BasicAuthentication]
 #   permission_classes = [IsAuthenticated]

 #   def post(self, request, pk, format=None):
        """
        Enroll the authenticated user in the course identified by `pk`.

        This method will:
        - Retrieve the course object using the primary key (`pk`).
        - Add the authenticated user (from the `request.user`) to the course's students.
        - Return a response indicating the user has been enrolled.

        Args:
            request (HttpRequest): The HTTP request object containing user details.
            pk (int): The primary key of the course to enroll in.
            format (str, optional): The response format (usually not needed).

        Returns:
            Response: A JSON response indicating whether the enrollment was successful.
        """
        # Retrieve the course by primary key, or return a 404 if not found
  #      course = get_object_or_404(Course, pk=pk)
        # Add the authenticated user to the course's students
  #      course.students.add(request.user)
        # Return a response indicating success
  #      return Response({'enrolled': True})
