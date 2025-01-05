"""
This module defines the view for handling chat room access within courses.

The `course_chat_room` view ensures that only authenticated users who are enrolled in the specified course
can access the chat room. It retrieves recent chat messages and renders the chat room template.

Functions:
    course_chat_room(request, course_id): Renders the chat room for a given course, accessible only
                                          to authenticated and enrolled users.
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render

from courses.models import Course


@login_required
def course_chat_room(request, course_id):
    """
    Handle the chat room view for a specific course.

    This view ensures that the currently logged-in user is enrolled in the specified course.
    If the user is not enrolled or the course does not exist, a 403 Forbidden response is returned.
    If the user is enrolled, the chat room page is rendered with the latest messages.

    Args:
        request: The HTTP request object.
        course_id: The ID of the course whose chat room is being accessed.

    Returns:
        HttpResponse: Renders the chat room template with the course and latest messages context.
        HttpResponseForbidden: If the user is not enrolled in the course or the course does not exist.
    """
    try:
        # Retrieve course with the given ID joined by the current user
        course = request.user.courses_joined.get(id=course_id)
    except Course.DoesNotExist:
        # User is not a student of the course or the course does not exist
        return HttpResponseForbidden()

    # Retrieve chat history
    latest_messages = course.chat_messages.select_related('user').order_by('-id')[:5]
    latest_messages = reversed(latest_messages)

    return render(
        request,
        'chat/room.html',
        {'course': course, 'latest_messages': latest_messages},
    )
