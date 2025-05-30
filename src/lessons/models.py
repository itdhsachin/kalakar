"""Module to perform database operations."""

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.loader import render_to_string

from accounts.models import User
from courses.fields import OrderField
from modules.models import Module
from courses.models import Course  
from assessment.models import StudentCompetition,CompetitionDetails



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

    def get_type(self):
        """Returns the readable lesson type."""
        return self.lesson_type.model.capitalize()


class LessonTrack(models.Model):
    """Tracks the progress of a lesson with an ID."""

    id = models.AutoField(primary_key=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="lesson_tracks")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lesson_tracks",null=True, blank=True)  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lesson_tracks",null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    state = models.BooleanField(default=True) 

    # # Fetching course ID through the lesson's module
    # @property
    # def get_course(self):
    #     return self.lesson.module.course if hasattr(self.lesson.module, "course") else None


    class Meta:
        verbose_name = "Attendance"
        verbose_name_plural = "Attendance"
        unique_together = ("user", "lesson")  # Ensures unique tracking per user per lesson

    def __str__(self):
        return f"Attendance for {self.user.username} on {self.lesson.id}"

# class LessonTracking(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)   
#     course_id = models.IntegerField()
#     access_on = models.DateTimeField(auto_now_add=True)
#     time_spent = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
#     is_complete = models.BooleanField(default=False)

#     def __str__(self):
#         return f"User {self.user.username} - Lesson {self.lesson_id} - {self.access_on}"

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

    def render(self, lesson, request):
        """Renders the item to a string using a template."""
        template_name = f"lessons/layouts/{self._meta.model_name}.html"
        course = lesson.module.course if hasattr(lesson.module, "course") else None
        competition_details = CompetitionDetails.objects.first()

        total_lessons_required = competition_details.total_lessons_required if competition_details else 20

        # Initialize defaults
        attended_lessons = 0
        attendance_percentage = 0
        is_eligible = False

        if request.user.is_authenticated:
            attended_lessons = LessonTrack.objects.filter(user=request.user, course=course).count()
            attendance_percentage = (attended_lessons / total_lessons_required) * 100 if total_lessons_required > 0 else 0
            is_eligible = attendance_percentage >= 50

        show_eligibility_message = False
        if lesson.object_id == total_lessons_required:
            show_eligibility_message = is_eligible

        return render_to_string(
            template_name,
            {
                "item": self,
                "course_id": lesson.module.course.id if hasattr(lesson.module, "course") else None,
                "user_id": request.user.id if request.user.is_authenticated else None,
                "lesson_id": lesson.id,
                "course_title": lesson.module.course.title,
                "lesson_title": lesson.title,
                "show_eligibility_message": show_eligibility_message,
            },
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


# class Video(ItemBase):
#     """Represents a video item with a URL field."""
#     url = models.URLField()
#     lessons = GenericRelation("Lesson", related_query_name="videos") 

# class Text(ItemBase):
#     """Represents a text item with content."""
#     content = models.TextField()
#     lessons = GenericRelation("Lesson", related_query_name="texts")  

# class Image(ItemBase):
#     """Represents an image item with an image field."""
#     image = models.ImageField(upload_to="images")
#     lessons = GenericRelation("Lesson", related_query_name="images")  

# class File(ItemBase):
#     """Represents a file item with a file field."""
#     file = models.FileField(upload_to="files")
#     lessons = GenericRelation("Lesson", related_query_name="files")