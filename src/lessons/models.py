"""Module to perform database operations."""

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.loader import render_to_string

from courses.fields import OrderField
from modules.models import Module


class Lesson(models.Model):
    """Represents a lesson within a module with an ID."""

    id = models.AutoField(primary_key=True, help_text="Primary key")
    title = models.CharField(
        max_length=255, null=False, help_text="Name of the lesson"
    )
    description = models.TextField(
        blank=True, null=True, help_text="Description of the lesson"
    )
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="lessons",
        help_text="Module this lesson belongs to",
    )

    lesson_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={"model__in": ("text", "video", "image", "file")},
    )

    object_id = models.PositiveIntegerField()
    item = GenericForeignKey("lesson_type", "object_id")

    prerequisite_lesson = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subsequent_lessons",
        help_text="Prerequisite lesson",
    )
    target_date = models.DateField(
        null=True, blank=True, help_text="Target date for the lesson"
    )
    available_date = models.DateField(
        null=True, blank=True, help_text="Available date for the lesson"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_lessons",
        help_text="User who created the lesson",
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp of the last update"
    )
    state = models.BooleanField(
        default=True, help_text="State of the lesson (active/inactive)"
    )

    order = OrderField(blank=True, for_fields=["module"])

    class Meta:
        """Metaclass."""

        ordering = ["order"]

    def __str__(self):
        """Returns the string representation of the Lesson."""
        return str(self.title)


class LessonTrack(models.Model):
    """Tracks the progress of a lesson with an ID."""

    id = models.AutoField(primary_key=True, help_text="Primary key")
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="lesson_tracks",
        help_text="Lesson being tracked",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="lesson_tracks",
        help_text="User who is tracking the lesson",
    )
    time_spent = models.IntegerField(
        default=0, help_text="Time spent on the lesson"
    )
    completed_at = models.DateTimeField(
        null=True, blank=True, help_text="Timestamp of completion"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp of creation"
    )
    state = models.BooleanField(
        default=True, help_text="State of the lesson track (active/inactive)"
    )

    def __str__(self):
        """Returns the string representation of the LessonTrack."""
        return f"LessonTrack for {self.user.username} on {self.lesson.id}"


class ItemBase(models.Model):
    """Abstract base class for different types of items with an owner, title, created and updated timestamps."""

    created_by = models.ForeignKey(
        User, related_name="%(class)s_related", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Metaclass."""

        abstract = True

    def __str__(self):
        """Returns the string representation of the item."""
        return str(self.title)

    def render(self):
        """Renders the item to a string using a template."""
        return render_to_string(
            f"courses/content/{self._meta.model_name}.html", {"item": self}
        )


class Text(ItemBase):
    """Represents a text item with content."""

    content = models.TextField()


class File(ItemBase):
    """Represents a file item with a file field."""

    file = models.FileField(upload_to="files")


class Image(ItemBase):
    """Represents an image item with an image field."""

    image = models.ImageField(upload_to="images")


class Video(ItemBase):
    """Represents a video item with a URL field."""

    url = models.URLField()
