from django.forms.models import inlineformset_factory

from modules.models import Module

from .models import Course

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
