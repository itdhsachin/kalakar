from django.contrib import admin
from assessment.models import StudentCompetition, AssessmentUpload

admin.site.register(StudentCompetition)

@admin.register(AssessmentUpload)
class AssessmentUploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'filename', 'content_type')
    readonly_fields = ('work',)