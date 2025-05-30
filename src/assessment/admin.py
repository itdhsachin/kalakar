from django.contrib import admin
from assessment.forms import AssessmentUploadForm
from django.db import connection  # Needed for raw SQL queries
from assessment.models import AssessmentUpload, StudentCompetition,CompetitionDetails

from django.utils.html import format_html
import base64
from django.http import HttpResponse
from django.urls import reverse

from django.forms import widgets, ModelForm


class DistrictFilter(admin.SimpleListFilter):
    """Custom filter for districts from the hardcoded MySQL table"""
    title = "District"
    parameter_name = "district"

    def lookups(self, request, model_admin):
        """Fetch districts directly from the MySQL table"""
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name FROM accounts_district ORDER BY name ASC")  # Ensure column names match DB
            districts = cursor.fetchall()
        
        return [(str(row[0]), row[1]) for row in districts]  # Convert results to (id, name) pairs

    def queryset(self, request, queryset):
        """Filter users by selected district"""
        if self.value():
            return queryset.filter(user_id_id__student_id__district_id=self.value())  # Ensure correct field reference

        return queryset  # Return full dataset if no filter applied

@admin.register(StudentCompetition)
class StudentCompetitionAdmin(admin.ModelAdmin):
    """Admin interface for managing student competitions."""

    list_display = ("user", "status", "created_date")
    list_filter = ("status",)
    search_fields = ("user__username",)


# @admin.register(AssessmentUpload)
# class AssessmentUploadAdmin(admin.ModelAdmin):
#     """Admin interface for managing assessment uploads."""

#     list_display = (
#         "user_id",
#         "filename",
#         "assigned_teacher",
#         "review_score",
#         "timestamp",
#     )
#     list_filter = ("assigned_teacher", "review_score")
#     search_fields = ("user_id__username", "assigned_teacher__username")
#     ordering = ("-timestamp",)
#     list_editable = ("assigned_teacher",)  # Allow admin to assign a teacher
# @admin.register(AssessmentUpload)
# class AssessmentUploadAdmin(admin.ModelAdmin):
#     """Admin interface for managing assessment uploads."""

#     list_display = (
#         "get_user",
#         "get_filename",
#         "assigned_teacher",
#         "review_score",
#         "timestamp",
#     )
#     list_filter = ("assigned_teacher", "review_score")
#     search_fields = ("user__username", "assigned_teacher__username")
#     ordering = ("-timestamp",)
#     list_editable = ("assigned_teacher",)
#     list_per_page = 10
#     list_select_related = ("user_id", "assigned_teacher")  # 

#     def get_filename(self, obj):
#         return obj.filename if obj.filename else ""
#     get_filename.short_description = "Filename"

#     def get_user(self, obj):
#         return obj.user_id.username
#     get_user.short_description = "User"


@admin.register(AssessmentUpload)
class AssessmentUploadAdmin(admin.ModelAdmin):
    list_display = (
        "get_user",
        "get_district",
        "display_image",
        "get_filename",
        "assigned_teacher",
        "review_score",
        "timestamp",
    )
    form = AssessmentUploadForm 
    readonly_fields = ("display_image",)

    list_filter = ("assigned_teacher", "review_score", DistrictFilter)
    search_fields = ("user_id__username", "assigned_teacher__username")
    ordering = ("-timestamp",)
    list_editable = ("assigned_teacher",)
    list_per_page = 10

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     return qs.select_related("user_id", "assigned_teacher").only(
    #         "user_id__username",
    #         "work",
    #         "filename",
    #         "assigned_teacher__username",
    #         "review_score",
    #         "timestamp"
    #     )
    def get_queryset(self, request):
        """Apply district filter from request GET parameters"""
        qs = super().get_queryset(request)
        qs = qs.select_related("user_id", "assigned_teacher")

        # Apply district filter if exists
        district_id = request.GET.get("district")
        if district_id:
            qs = qs.filter(user_id_id__student_id__district_id=district_id)

        return qs

    def get_filename(self, obj):
        return obj.filename if obj.filename else ""
    get_filename.short_description = "Filename"

    def get_user(self, obj):
        return obj.user_id.username
    get_user.short_description = "User"

    def get_district(self, obj):
        """Fetch district name from accounts_district"""
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT name FROM accounts_district WHERE id = (SELECT district_id FROM accounts_student WHERE student_id = %s)",
                [obj.user_id_id]  # Assuming user_id_id refers to the student's ID
            )
            district = cursor.fetchone()
        
        return district[0] if district else "Not Assigned"

    get_district.short_description = "District"
    get_district.admin_order_field = "user_id_id__student_id__district_id"  # allow sorting

    def display_image(self, obj):
        """Render clickable image to download or open in new tab"""
        if obj.work:
            url = '#'
            return format_html(
                '<a href="{}" target="_blank"><img src="data:image/png;base64,{}" width="400" height="auto"/></a>',
                url,
                base64.b64encode(obj.work).decode("utf-8")
            )
        return "No Image"

    display_image.short_description = "Work Image"

@admin.register(CompetitionDetails)
class CompetitionDetailsAdmin(admin.ModelAdmin):
    """Admin interface for managing competition details."""

    list_display = ("total_lessons_required", "course_end_date")
    ordering = ("-course_end_date",)