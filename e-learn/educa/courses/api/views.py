from django.db.models import Count
from rest_framework import generics
from rest_framework import viewsets
from courses.models import Course, Subject
from courses.api.pagination import StandardPagination
from courses.api.serializers import CourseSerializer, SubjectSerializer

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
