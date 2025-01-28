"""Module to enable admin functionality."""

from django.contrib import admin

from courses.models import Course, Subject
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

    list_display = ["title", "subject", "created_by"]
    list_filter = ["created_by", "subject"]
    search_fields = ["title", "description"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ModuleInline]
