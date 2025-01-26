from django.contrib import admin

from modules.models import Module

from .models import Course, Subject

# admin.site.index_template = 'memcache_status/admin_index.html';


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ["title", "slug"]
    prepopulated_fields = {"slug": ("title",)}


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "subject", "created_by"]
    list_filter = ["created_by", "subject"]
    search_fields = ["title", "description"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ModuleInline]
