"""Views for the lessons app.

This module contains view functions for rendering lesson details in the lessons application.
"""

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View

from courses.models import Enrollment
from lessons.models import Lesson


class LessonDetailView(View):
    """View to display the details of a lesson.

    Methods:
        get(request, *args, **kwargs): Handle GET requests to display lesson details.
    """

    def get(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        """Handle GET requests to display lesson details.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: The HTTP response with the rendered lesson content.
        """
        lesson_id = kwargs.get("pk")
        lesson = get_object_or_404(Lesson, id=lesson_id)
        course = lesson.module.course

        # Check if the lesson and course are active
        if not lesson.state or not course.state:
            raise PermissionDenied()

        # Check if the user is enrolled in the course and the enrollment is active
        enrollment = Enrollment.objects.filter(
            user=request.user, course=course, state=True
        ).first()

        if not enrollment:
            return redirect("courses", slug=course.slug)

        # Render the content using the render method from ItemBase
        rendered_content = lesson.item.render()

        return HttpResponse(rendered_content)
