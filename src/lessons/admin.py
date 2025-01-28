"""Admin Module."""

from django.contrib import admin

from lessons.models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Lesson admin config."""

    list_display = ["title", "description", "module", "lesson_type"]
    list_filter = ["module", "lesson_type"]
    search_fields = ["title", "description"]
