"""App configuration for the accounts app.

This module contains the AppConfig class for the accounts application, which handles
the app's configuration and ready method.
"""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Configuration for the accounts app.

    Attributes:
        default_auto_field (str): The default auto field type for models.
        name (str): The name of the app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self) -> None:
        """Perform initialization tasks when the app is ready.

        This method connects the post_save signal to the post_save_account_receiver
        function for the User model.
        """
        from django.db.models.signals import post_save

        from accounts.models import User
        from accounts.signals import post_save_account_receiver

        post_save.connect(post_save_account_receiver, sender=User)

        return super().ready()
