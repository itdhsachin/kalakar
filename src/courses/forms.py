"""Module."""

from django.forms.models import inlineformset_factory

from courses.models import Course
from modules.models import Module

# Define the ModuleFormSet with inline formset factory
ModuleFormSet = inlineformset_factory(
    Course,
    Module,
    fields=[
        "title",
        "description",
        "target_end_date",
        "start_date",
        "prerequisite_module",
    ],
    extra=2,
    can_delete=True,
)
