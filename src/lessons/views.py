"""Views for the lessons app.

This module contains view functions for rendering lesson details in the lessons application.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View
from courses.models import Enrollment
from lessons.models import Lesson,LessonTrack
from django.utils.timezone import now
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


class LessonDetailView(View):
    """View to display the details of a lesson.

    Methods:
        get(request, *args, **kwargs): Handle GET requests to display lesson details.
    """
    # login_url = "accounts/login/"  
    # redirect_field_name = "login" 
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
        # enrollment = Enrollment.objects.filter(
        #     user=request.user, course=course, state=True
        # ).first()

        # if not enrollment:
        #     return redirect("courses", slug=course.slug)
        # LessonTrack.objects.update_or_create(
        #     user=request.user,
        #     lesson=lesson,
        #     defaults={
        #         "created_at": now(),
        #         "state": True
        #     }
        # )
        # Render the content using the render method from ItemBase
        if lesson.item is None:
            return HttpResponse(
                "<h2>Sorry, this lesson will be available soon. Please check back later. <br> We appreciate your patience!</h2>",
                status=200,
                )
        rendered_content = lesson.item.render(lesson,request)

        return HttpResponse(rendered_content)

@login_required
def track_lesson(request):
    """Handles AJAX requests to track lesson attendance."""
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        lesson_id = request.POST.get("lesson_id")
        user_id = request.POST.get("user_id")  # Fetch user ID from AJAX

        if not lesson_id:
            return JsonResponse({"status": "error", "message": "Missing lesson ID"}, status=400)

        if not user_id:
            return JsonResponse({"status": "error", "message": "Missing user ID"}, status=400)

        lesson = get_object_or_404(Lesson, id=lesson_id)

        # Get the course ID from the lesson's module
        course = lesson.module.course if hasattr(lesson.module, "course") else None
        if course is None:
            return JsonResponse({"status": "error", "message": "Course ID not found"}, status=400)

        # Insert or update attendance record
        lesson_track, created = LessonTrack.objects.get_or_create(
            user_id=user_id,  # Directly use user_id instead of fetching User object
            lesson=lesson,
            defaults={
                "created_at": now(),
                "course": course  
            }
        )

        # If the record already existed, ensure course is updated
        if not created and lesson_track.course is None:
            lesson_track.course = course
            lesson_track.save()

        return JsonResponse({
            "status": "success",
            "message": "Lesson tracked successfully",
            "lesson_id": lesson_id,
            "course_id": course.id,
            "user_id": user_id,
            "created": created
        })

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)