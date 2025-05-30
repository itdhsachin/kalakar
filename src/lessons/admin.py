from django.contrib import admin
from lessons.models import Lesson, LessonTrack

class LessonTrackInline(admin.TabularInline):
    """Inline view for lesson tracking."""
    model = LessonTrack
    extra = 0  

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Lesson admin configuration."""
    
    list_display = ["title", "available_date", "description", "module", "lesson_type"]
    list_filter = ["module", "lesson_type"]
    search_fields = ["title", "description"]
    inlines = [LessonTrackInline]  # Add inline tracking for LessonTrack

@admin.register(LessonTrack)
class LessonTrackAdmin(admin.ModelAdmin):
    """Lesson tracking admin view."""
    
    list_display = ("user", "lesson", "course", "created_at", "completed_at", "state")
    list_filter = ("course", "state", "created_at")
    search_fields = ("user__username", "lesson__title", "course__title")
    ordering = ("-created_at",)
    readonly_fields = ("user", "lesson", "course", "created_at")

