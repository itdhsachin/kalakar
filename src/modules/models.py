"""Module database models."""

from django.db import models

from accounts.models import User
from courses.fields import OrderField
from courses.models import Course


class Module(models.Model):
    """Represents a module within a course with an ID."""

    id = models.AutoField(primary_key=True, help_text="Primary key")
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="modules",
        help_text="Course this module belongs to",
    )
    title = models.CharField(
        max_length=255, null=False, help_text="Title of the module"
    )
    description = models.TextField(
        blank=True, null=True, help_text="Description of the module"
    )
    target_end_date = models.DateField(
        null=True, blank=True, help_text="Target end date for the module"
    )
    start_date = models.DateField(
        null=True, blank=True, help_text="Start date for the module"
    )
    prerequisite_module = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subsequent_modules",
        help_text="Prerequisite module",
    )
    order = OrderField(
        blank=True, help_text="Order of the module within the course"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_modules",
        help_text="User who created the module",
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp of the last update"
    )
    state = models.BooleanField(
        default=True, help_text="State of the module (active/inactive)"
    )

    def __str__(self):
        """Returns the string representation of the Module."""
        return str(self.title)

    class Meta:
        """meta class."""

        ordering = ["order"]


class ModuleTrack(models.Model):
    """Tracks the progress of a module with a module."""

    id = models.AutoField(primary_key=True, help_text="Primary key")
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="module_tracks",
        help_text="Module being tracked",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="module_tracks",
        help_text="User who is tracking the module",
    )
    time_spent = models.IntegerField(
        default=0, help_text="Time spent on the module"
    )
    is_completed = models.BooleanField(
        default=False, help_text="Indicates if the module is completed"
    )
    completed_at = models.DateTimeField(
        null=True, blank=True, help_text="Timestamp of completion"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp of creation"
    )
    state = models.BooleanField(
        default=True, help_text="State of the module track (active/inactive)"
    )

    def __str__(self):
        """Returns the string representation of the ModuleTrack."""
        return f"ModuleTrack for {self.user.username} on {self.module.title}"
