"""App config module."""

from django.apps import AppConfig


class StudentsConfig(AppConfig):
    """Configuration for the students' app.

    Attributes:
        name (str): The name of the app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "students"
