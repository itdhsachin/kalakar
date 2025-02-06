"""Admin configuration for the accounts app.

This module contains the admin interface options for the User and Student models.
"""

from django.contrib import admin

from accounts.models import Student, User, Teacher



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

class TeacherAdmin(admin.ModelAdmin):
    """Admin interface for Teacher"""
    list_display = ['teacher', 'get_full_name','username',]
    search_fields = ['teacher__username', 'teacher__first_name', 'teacher__last_name', 'teacher__email']

    class Meta:
        managed = True
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"

admin.site.register(User, UserAdmin)
admin.site.register(Student)
admin.site.register(Teacher)
