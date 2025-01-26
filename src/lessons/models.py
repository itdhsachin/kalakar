"""Module to perform database operations."""

from django.contrib.auth.models import User
from django.db import models

from modules.models import Module


class LessonTypeMaster(models.Model):
    """Represents the master data for lesson types with an ID."""

    id = models.AutoField(primary_key=True, help_text="Primary key")
    type = models.CharField(
        max_length=255, null=False, help_text="Type of lesson"
    )
    description = models.TextField(
        blank=True, null=True, help_text="Description of the lesson type"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_lesson_types",
        help_text="User who created the lesson type",
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp of the last update"
    )

    def __str__(self):
        """Returns the string representation of the LessonTypeMaster."""
        return str(self.type)


class Lesson(models.Model):
    """Represents a lesson within a module with an ID."""

    id = models.AutoField(primary_key=True, help_text="Primary key")
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="lessons",
        help_text="Module this lesson belongs to",
    )
    lesson_type = models.ForeignKey(
        LessonTypeMaster,
        on_delete=models.CASCADE,
        related_name="lessons",
        help_text="Type of the lesson",
    )
    content_url = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="URL of the lesson content",
    )
    order = models.IntegerField(
        null=False, help_text="Order of the lesson within the module"
    )
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

    def __str__(self):
        """Returns the string representation of the Lesson."""
        return str(self.content_url)


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
