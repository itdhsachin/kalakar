"""Views for the pages app.

This module contains view functions for rendering pages in the pages application.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template.exceptions import TemplateDoesNotExist


@login_required
def index_page_view(request):
    """Render the index page.

    This view function renders the index.html template. If the template does not exist,
    it renders an error page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response with the rendered template.
    """
    try:
        return render(request, "pages/index.html")
    except TemplateDoesNotExist:
        return render(request, "pages/error.html")


@login_required
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
