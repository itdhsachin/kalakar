from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom User model extending AbstractUser."""

    pass  # You can add custom fields if needed

    class Meta:
        swappable = "AUTH_USER_MODEL"
