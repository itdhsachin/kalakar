# admin.py
from django import forms
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from lessons.models import Lesson, LessonTrack, Video
from django.utils.translation import gettext_lazy as _

class LessonTrackInline(admin.TabularInline):
    model = LessonTrack
    extra = 0

class LessonForm(forms.ModelForm):
    video_url = forms.URLField(
        required=False,
        label=_("Video URL"),
        help_text=_("Only used if lesson_type is Video")
    )

    class Meta:
        model = Lesson
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        inst = kwargs.get("instance") or getattr(self, "instance", None)
        # Prefill video url when the Lesson points to a Video
        if inst and inst.pk and hasattr(inst, "item") and isinstance(inst.item, Video):
            self.fields["video_url"].initial = inst.item.url

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    form = LessonForm
    list_display = ["title", "available_date", "target_date", "release_after_days", "description", "module", "lesson_type", "get_video_url"]
    list_filter = ["module", "lesson_type"]
    search_fields = ["title", "description"]
    inlines = [LessonTrackInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(module__course__state=1)
    
    def get_video_url(self, obj):
        if hasattr(obj, "item") and isinstance(obj.item, Video):
            return obj.item.url
        return "-"
    get_video_url.short_description = "Video URL"
    get_video_url.admin_order_field = "object_id"  # optional if you want ordering
    
    def save_model(self, request, obj, form, change):
        """
        Create or update the underlying Video item when lesson_type is Video.
        We need request to populate created_by on Video.
        """
        # Ensure created_by for new lessons
        if not obj.pk and not getattr(obj, "created_by_id", None):
            obj.created_by = request.user

        # Decide if this lesson refers to Video type
        video_ct = ContentType.objects.get_for_model(Video)
        video_url = form.cleaned_data.get("video_url", "").strip()

        if obj.lesson_type == video_ct:
            # Update existing Video if present
            if change and hasattr(obj, "item") and isinstance(obj.item, Video):
                video = obj.item
                video.url = video_url
                video.title = obj.title or video.title
                if not getattr(video, "created_by_id", None):
                    video.created_by = request.user
                video.save()
                obj.object_id = video.pk
            else:
                # create a new Video and attach it
                video = Video.objects.create(
                    created_by=request.user,
                    title=obj.title or "Video for lesson",
                    url=video_url
                )
                obj.object_id = video.pk
                obj.lesson_type = video_ct

        # if lesson_type is not video, we leave item/object_id as-is (or you can clear it)
        super().save_model(request, obj, form, change)
