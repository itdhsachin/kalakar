"""Admin configuration for the accounts app.

This module contains the admin interface options for the User, Student, and Teacher models.
"""

from django.contrib import admin, messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import path
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from accounts.models import Student, Teacher, User,State,District

import csv
from django.http import HttpResponse

class UserAdmin(admin.ModelAdmin):
    """Admin interface options for the User model."""

    list_display = [
        "get_full_name",
        "username",
        "phone",
        "email",
        "is_active",
        "is_student",
        "is_lecturer",
        "is_staff",
        "delete_button",
    ]
    search_fields = ["username", "phone", "first_name", "last_name", "email"]
    actions = ["export_as_csv"]

    def delete_button(self, obj):
        """Generate a delete button for each user row."""
        return format_html(
            '<a class="button" style="color:white;" href="delete_user/?id={}">Delete</a>',
            obj.id,
        )

    delete_button.short_description = "Delete"

    def get_urls(self):
        """Add custom URL for deleting a user."""
        urls = super().get_urls()
        custom_urls = [
            path("delete_user/", self.admin_site.admin_view(self.delete_user)),
        ]
        return custom_urls + urls

    def delete_user(self, request):
        """Handles user deletion."""
        user_id = request.GET.get("id", None)

        if not user_id:
            messages.error(request, _("User ID not provided."))
            return redirect("/admin/accounts/user/")

        try:
            user = User.objects.get(id=user_id)
            user.delete()
            messages.success(request, _("User deleted successfully."))
        except ObjectDoesNotExist:
            messages.error(request, _("User not found."))

        return redirect("/admin/accounts/user/")

    def export_as_csv(self, request, queryset):
        """Export selected users as CSV with email, phone, full name."""
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="users.csv"'

        writer = csv.writer(response)
        writer.writerow(["Full Name", "Email", "Phone"])  # CSV headers

        for user in queryset:
            writer.writerow([user.get_full_name(), user.email, user.phone])

        return response

    export_as_csv.short_description = "Export Selected Users as CSV"
    
    class Meta:
        managed = True
        verbose_name = "User"
        verbose_name_plural = "Users"


class TeacherAdmin(admin.ModelAdmin):
    """Admin interface for Teacher."""

    list_display = [
        "teacher",
        "get_full_name",
        "username",
        "email",
        "delete_button",
    ]
    search_fields = [
        "teacher__username",
        "teacher__first_name",
        "teacher__last_name",
        "teacher__email",
    ]

    def get_full_name(self, obj):
        """Get full name from related User model."""
        return obj.teacher.get_full_name()

    def username(self, obj):
        """Get username from related User model."""
        return obj.teacher.username

    def email(self, obj):
        """Get email from related User model."""
        return obj.teacher.email

    get_full_name.admin_order_field = "teacher__first_name"
    get_full_name.short_description = "Full Name"

    username.admin_order_field = "teacher__username"
    username.short_description = "Username"

    email.admin_order_field = "teacher__email"
    email.short_description = "Email"

    def delete_button(self, obj):
        """Generate a delete button for each teacher row."""
        return format_html(
            '<a class="button" style="color:white;" href="delete_teacher/?id={}">Delete</a>',
            obj.id,
        )

    delete_button.short_description = "Delete"

    def get_urls(self):
        """Add custom URL for deleting a teacher."""
        urls = super().get_urls()
        custom_urls = [
            path(
                "delete_teacher/",
                self.admin_site.admin_view(self.delete_teacher),
            ),
        ]
        return custom_urls + urls

    def delete_teacher(self, request):
        """Handles teacher deletion."""
        teacher_id = request.GET.get("id", None)

        if not teacher_id:
            messages.error(request, _("Teacher ID not provided."))
            return redirect("/admin/accounts/teacher/")

        try:
            teacher = Teacher.objects.get(id=teacher_id)
            teacher.delete()
            messages.success(request, _("Teacher deleted successfully."))
        except ObjectDoesNotExist:
            messages.error(request, _("Teacher not found."))

        return redirect("/admin/accounts/teacher/")

    class Meta:
        managed = True
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"


class StudentAdmin(admin.ModelAdmin):
    """Admin interface for Student."""

    list_display = [
        "student",
        "get_full_name",
        "username",
        "email",
        "delete_button",
    ]
    search_fields = [
        "student__username",
        "student__first_name",
        "student__last_name",
    ]

    def get_full_name(self, obj):
        """Get full name from related User model."""
        return obj.student.get_full_name()

    def username(self, obj):
        """Get username from related User model."""
        return obj.student.username

    def email(self, obj):
        """Get email from related User model."""
        return obj.student.email

    get_full_name.admin_order_field = "student__first_name"
    get_full_name.short_description = "Full Name"

    username.admin_order_field = "student__username"
    username.short_description = "Username"

    email.admin_order_field = "student__email"
    email.short_description = "Email"

    def delete_button(self, obj):
        """Generate a delete button for each student row."""
        return format_html(
            '<a class="button" style="color:white;" href="delete_student/?id={}">Delete</a>',
            obj.id,
        )

    delete_button.short_description = "Delete"

    def get_urls(self):
        """Add custom URL for deleting a student."""
        urls = super().get_urls()
        custom_urls = [
            path(
                "delete_student/",
                self.admin_site.admin_view(self.delete_student),
            ),
        ]
        return custom_urls + urls

    def delete_student(self, request):
        """Handles student deletion."""
        student_id = request.GET.get("id", None)

        if not student_id:
            messages.error(request, _("Student ID not provided."))
            return redirect("/admin/accounts/student/")

        try:
            student = Student.objects.get(id=student_id)
            student.delete()
            messages.success(request, _("Student deleted successfully."))
        except ObjectDoesNotExist:
            messages.error(request, _("Student not found."))

        return redirect("/admin/accounts/student/")

    class Meta:
        managed = True
        verbose_name = "Student"
        verbose_name_plural = "Students"


class StateAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)

class DistrictAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "state")
    search_fields = ("name", "state__name")
    list_filter = ("state",)
    ordering = ("state", "name")
# Register models with admin panel
admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(District, DistrictAdmin)
