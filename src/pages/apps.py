"""App configuration for the pages app.

This module contains the AppConfig class for the pages application, which handles
the app's configuration.
"""

from django.apps import AppConfig


class PagesConfig(AppConfig):
    """Configuration for the pages app.

    Attributes:
        default_auto_field (str): The default auto field type for models.
        name (str): The name of the app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "pages"
