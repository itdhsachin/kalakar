"""Form module."""

from django import forms

from courses.models import Course


class CourseEnrollForm(forms.Form):
    """Form for enrolling in a course.

    Attributes:
        course (ModelChoiceField): A hidden field to select a course.
    """

    course = forms.ModelChoiceField(
        queryset=Course.objects.all(), widget=forms.HiddenInput
    )
