from django.contrib import admin
from .models import StudentCompetition, AssessmentUpload

@admin.register(StudentCompetition)
class StudentCompetitionAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'created_date')
    list_filter = ('status',)
    search_fields = ('user__username',)

@admin.register(AssessmentUpload)
class AssessmentUploadAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'filename', 'assigned_teacher', 'review_score', 'timestamp')
    list_filter = ('assigned_teacher', 'review_score')
    search_fields = ('user_id__username', 'assigned_teacher__username')
    ordering = ('-timestamp',)
    list_editable = ('assigned_teacher',)  # Allow admin to assign a teacher
