"""Views for the pages app.

This module contains view functions for rendering pages in the pages application.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template.exceptions import TemplateDoesNotExist
from django.http import HttpResponse
from courses.models import Course,Enrollment  
from django.utils import timezone
from django.db.models import Q


def index_page_view(request):
    try:
        today = timezone.now().date()  # Get only the date part

        # Filter courses with enroll_end_date >= today
        courses = Course.objects.filter(
            state=1
        ).filter(
            Q(enroll_end_date__gte=today) | Q(enroll_end_date__isnull=True)
        ).order_by("id")[:12]
        # courses = Course.objects.filter(state=1).order_by("id")[:8]  # limit to 8

        purchased_course_ids = set()
        if request.user.is_authenticated:
            purchased_course_ids = set(
                Enrollment.objects.filter(user=request.user).values_list("course_id", flat=True)
            )

        context = {
            'courses': courses,
            'purchased_course_ids': purchased_course_ids, 
            'today': today,
        }
        return render(request, "pages/index.html", context)

    except TemplateDoesNotExist:
        return render(request, "pages/error.html")


def dynamic_pages_view(request, template_name):
    """Render a dynamic page based on the template name.

    This view function renders the specified template. If the template does not exist,
    it renders an error page.

    Args:
        request (HttpRequest): The HTTP request object.
        template_name (str): The name of the template to render.

    Returns:
        HttpResponse: The HTTP response with the rendered template.
    """
    try:
        return render(request, f"pages/{template_name}.html")
    except TemplateDoesNotExist:
        return render(request, "pages/error.html")


def terms_condition(request):
    try:
        return render(request, "pages/terms_condition.html")
    except TemplateDoesNotExist:
        return render(request, "pages/error.html")
def privacy_policy(request):
    try:
        return render(request, "pages/privacy_policy.html")
    except TemplateDoesNotExist:
        return render(request, "pages/error.html")
def competition_one_result(request):
    try:
        return render(request, "pages/competition_one_result.html")
    except TemplateDoesNotExist:
        return render(request, "pages/error.html")        
def faq(request):
    try:
        return render(request, "pages/faq.html")
    except TemplateDoesNotExist:
        return render(request, "pages/error.html")


def robots_txt(request):
    content = """User-agent: *
Disallow: /admin/
Disallow: /accounts/
Sitemap: https://kalagurubyirarangoliarts.com/sitemap.xml
"""
    return HttpResponse(content, content_type="text/plain")