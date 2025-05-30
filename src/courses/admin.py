"""Module to enable admin functionality."""

from django.contrib import admin

from courses.models import Course, Subject,Enrollment
from modules.models import Module

# admin.site.index_template = 'memcache_status/admin_index.html';


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Admin view for managing Subject instances.

    Attributes:
        list_display (list): Fields to display in the list view.
        prepopulated_fields (dict): Fields to prepopulate based on other fields.
    """

    list_display = ["title", "slug"]
    prepopulated_fields = {"slug": ("title",)}


class ModuleInline(admin.StackedInline):
    """Inline admin descriptor for Module model.

    Attributes:
        model (Model): The model to be used inline.
    """

    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Admin view for managing Course instances.

    Attributes:
        list_display (list): Fields to display in the list view.
        list_filter (list): Fields to filter the list view.
        search_fields (list): Fields to search in the list view.
        prepopulated_fields (dict): Fields to prepopulate based on other fields.
        inlines (list): Inline models to be displayed within the admin view.
    """

    list_display = ["title", "enroll_end_date", "price", "state", "subject", "created_by"]
    list_filter = ["created_by", "subject"]
    search_fields = ["title", "description"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ModuleInline]

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("user", "user_id", "course", "enrollment_date", "is_completed", "state")
    list_filter = ("is_completed", "state", "enrollment_date")
    search_fields = ("user__username", "course__title")
    autocomplete_fields = ("user", "course", "created_by")
    readonly_fields = ("updated_at", "enrollment_date")

    fieldsets = (
        (None, {
            "fields": ("user", "course", "created_by", "target_end_date", "is_completed", "completion_date", "state")
        }),
        ("Timestamps", {
            "fields": ("enrollment_date", "updated_at")
        }),
    )
