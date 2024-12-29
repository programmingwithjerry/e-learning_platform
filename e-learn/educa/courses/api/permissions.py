from rest_framework.permissions import BasePermission

class IsEnrolled(BasePermission):
    """
    Custom permission to check if the user is enrolled in a specific course.

    This permission class is used to check if the authenticated user is enrolled in
    the course (or other object) they are attempting to access. It checks whether
    the user is included in the `students` field (a many-to-many relationship) of the
    object (e.g., a course) that the user is trying to access.

    Methods:
        has_object_permission: Checks if the user is enrolled in the course (or object) by filtering
                                the `students` related field on the object.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the authenticated user is enrolled in the course (or object).

        This method checks whether the user making the request is included in the `students`
        many-to-many relationship field of the given object (e.g., the `Course` object). The
        user is considered enrolled if their ID exists in the list of students associated with the object.

        Args:
            request (HttpRequest): The HTTP request object, which contains the authenticated user.
            view (View): The view handling the request (not used in this implementation).
            obj (Model): The object being accessed (e.g., a `Course` instance).

        Returns:
            bool: `True` if the user is enrolled (exists in the `students` list), `False` otherwise.
        """
        return obj.students.filter(id=request.user.id).exists()
