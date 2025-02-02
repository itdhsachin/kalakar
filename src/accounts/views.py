"""Views for the accounts app.

This module contains view functions for rendering profiles in the accounts application.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from accounts.models import Session, Student, User


@login_required
def profile(request):
    """Show profile of the current user.

    This view function renders the profile.html template with the context specific to the
    current user, including user-specific data and courses.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response with the rendered template.
    """
    current_session = Session.objects.filter(is_current_session=True).first()

    context = {
        "title": request.user.get_full_name,
        "current_session": current_session,
    }

    if request.user.is_lecturer:
        # @TODO add user courses in context
        # courses = Course.objects.filter(
        #     allocated_course__lecturer__pk=request.user.id, semester=current_semester
        # )
        # context["courses"] = courses

        return render(request, "accounts/profile.html", context)

    if request.user.is_student:
        get_object_or_404(Student, student__pk=request.user.id)
        # courses = TakenCourse.objects.filter(
        #     student__student__id=request.user.id, course__level=student.level
        # )

        # @TODO add user courses in context
        context.update(
            {
                # "courses": courses,
                # "level": student.level,
                "dummy": "dummy"
            }
        )
        return render(request, "accounts/profile.html", context)

    # For superuser or other staff
    staff = User.objects.filter(is_lecturer=True)
    context["staff"] = staff
    return render(request, "accounts/profile.html", context)
