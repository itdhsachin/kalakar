"""Admin configuration for the accounts app.

This module contains the admin interface options for the User and Student models.
"""

from django.contrib import admin

from accounts.models import Student, User


class UserAdmin(admin.ModelAdmin):
    """Admin interface options for the User model.

    Attributes:
        list_display (list): Fields to display in the admin list view.
        search_fields (list): Fields to include in the search functionality.

    Meta:
        managed (bool): Whether the model is managed by Django.
        verbose_name (str): Singular name for the User model.
        verbose_name_plural (str): Plural name for the User model.
    """

    list_display = [
        "get_full_name",
        "username",
        "email",
        "is_active",
        "is_student",
        "is_lecturer",
        "is_staff",
    ]
    search_fields = [
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "is_lecturer",
        "is_staff",
    ]

    class Meta:
        """Meta options for the UserAdmin class."""

        managed = True
        verbose_name = "User"
        verbose_name_plural = "Users"


admin.site.register(User, UserAdmin)
admin.site.register(Student)
