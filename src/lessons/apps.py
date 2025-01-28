"""Module to add lesson entry to app."""

from django.apps import AppConfig


class LessonsConfig(AppConfig):
    """Config class."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "lessons"
