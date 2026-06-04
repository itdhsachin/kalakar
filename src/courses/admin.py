"""Module to enable admin functionality."""

from django.contrib import admin

from courses.models import Course, Subject, Enrollment, Batch
from modules.models import Module
from django.http import HttpResponse
import csv

from accounts.models import Student 
from django.utils.html import format_html

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

    list_display = ["title", "enroll_end_date",  "price", "state", "subject", "created_by","course_image_tag"]
    list_filter = ["created_by", "subject"]
    search_fields = ["title", "description"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ModuleInline]

    def course_image_tag(self, obj):
        if obj.course_image:
            return format_html(
                '<img src="{}" width="200" height="150" style="object-fit:cover;" />', 
                obj.course_image.url
            )
        return "-"
    course_image_tag.short_description = "Course Image"

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "batch", "coupon_code", "enrollment_date", "is_completed", "state")
    list_filter = ("is_completed", "course", "coupon_code", "state", "enrollment_date")
    search_fields = ("user__username", "course__title", "coupon_code")
    autocomplete_fields = ("user", "course", "created_by")
    readonly_fields = ("updated_at", "enrollment_date")
    actions = ["export_as_csv"]

    fieldsets = (
        (None, {
            "fields": ("user", "course", "batch", "created_by", "target_end_date", "is_completed", "completion_date", "state")
        }),
        ("Timestamps", {
            "fields": ("enrollment_date", "updated_at")
        }),
    )

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="enrollments_with_students.csv"'

        writer = csv.writer(response)
        writer.writerow([
            "Username", "First Name", "Last Name", "User ID", "Email", "Phone", "Course", "Enrollment Date", "Is Completed", "State",
            # Student fields
            "Gender", "Birthday", "Education", "Address", "Taluka", "State", "Other State",
            "District", "Other District", "Pincode", "Hobbies"
        ])

        for enrollment in queryset.select_related("user", "course"):
            user = enrollment.user
            try:
                student = user.student  # or Student.objects.get(user=user)
            except Student.DoesNotExist:
                student = None

            writer.writerow([
                user.username if user else "",
                user.first_name if user else "",
                user.last_name if user else "",
                user.id if user else "",
                user.email if user else "",
                user.phone if user else "",
                enrollment.course.title if enrollment.course else "",
                enrollment.enrollment_date.strftime("%Y-%m-%d") if enrollment.enrollment_date else "",
                "Yes" if enrollment.is_completed else "No",
                enrollment.state or "",
                # Student fields
                getattr(student, "gender", ""),
                student.birthday.strftime("%Y-%m-%d") if student and student.birthday else "",
                getattr(student, "education", ""),
                getattr(student, "address", ""),
                getattr(student, "taluka", ""),
                getattr(student, "state", ""),
                getattr(student, "other_state", ""),
                getattr(student, "district", ""),
                getattr(student, "other_district", ""),
                getattr(student, "pincode", ""),
                getattr(student, "hobbies", "")
            ])

        return response

    export_as_csv.short_description = "Export selected enrollments with student data as CSV"

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ("name", "course", "start_date", "end_date", "state")
    list_filter = ("course", "state")
    search_fields = ("name",)