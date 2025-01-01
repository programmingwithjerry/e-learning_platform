from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from courses.models import Course


@login_required
def course_chat_room(request, course_id):
    """
    Handles the chat room view for a specific course.
    Args:
        request: The HTTP request object.
        course_id: The ID of the course to access the chat room.

    Return:
        An HTTP response rendering the chat room template if the course exists
        and the user is a member. Otherwise, returns an HTTP 403 Forbidden response.
    """
    try:
        # Attempt to retrieve the course with the given ID that the current user has joined.
        course = request.user.courses_joined.get(id=course_id)
    except Course.DoesNotExist:
        # If the course does not exist or the user is not enrolled in it, deny access.
        return HttpResponseForbidden()

    # Render the chat room template, passing the course as context.
    return render(request, 'chat/room.html', {'course': course})
