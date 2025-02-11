from django.contrib import admin

from assessment.models import AssessmentUpload, StudentCompetition


@admin.register(StudentCompetition)
class StudentCompetitionAdmin(admin.ModelAdmin):
    """Admin interface for managing student competitions."""

    list_display = ("user", "status", "created_date")
    list_filter = ("status",)
    search_fields = ("user__username",)


@admin.register(AssessmentUpload)
class AssessmentUploadAdmin(admin.ModelAdmin):
    """Admin interface for managing assessment uploads."""

    list_display = (
        "user_id",
        "filename",
        "assigned_teacher",
        "review_score",
        "timestamp",
    )
    list_filter = ("assigned_teacher", "review_score")
    search_fields = ("user_id__username", "assigned_teacher__username")
    ordering = ("-timestamp",)
    list_editable = ("assigned_teacher",)  # Allow admin to assign a teacher
