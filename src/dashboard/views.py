"""dashboard view file."""

from django.http import HttpResponse
from django.template import loader


# Create your views here.
def index(request):
    """Index function for reder base template."""
    # return render(request, './../templates/dashboard/index.html')
    template = loader.get_template("dashboard/index.html")
    context = {
        "val": "hello",
    }
    return HttpResponse(template.render(context, request))
