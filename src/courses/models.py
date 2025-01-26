"""Course database models."""

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.loader import render_to_string

from courses.fields import OrderField


class Subject(models.Model):
    """Represents a subject with a title and slug."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        """meta class."""

        ordering = ["title"]

    def __str__(self):
        """Returns the string representation of the Subject."""
        return str(self.title)


class Course(models.Model):
    """Represents a course with an owner, subject, title, overview, slug, created timestamp, and students."""

    owner = models.ForeignKey(
        User, related_name="courses_created", on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject, related_name="courses", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    overview = models.TextField()
    slug = models.CharField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(
        User, related_name="courses_joined", blank=True
    )

    class Meta:
        """meta class."""

        ordering = ["-created"]

    def __str__(self):
        """Returns the string representation of the Course."""
        return str(self.title)


class Module(models.Model):
    """Represents a module within a course with a title, description, and order."""

    course = models.ForeignKey(
        Course, related_name="modules", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=["course"])

    class Meta:
        """meta class."""

        ordering = ["order"]

    def __str__(self):
        """Returns the string representation of the Module."""
        return f"{self.order}, {self.title}"


class Content(models.Model):
    """Represents content within a module with a content type, object ID, and order."""

    module = models.ForeignKey(
        Module, related_name="contents", on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={"model__in": ("text", "video", "image", "file")},
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey("content_type", "object_id")
    order = OrderField(blank=True, for_fields=["module"])

    class Meta:
        """meta class."""

        ordering = ["order"]


class ItemBase(models.Model):
    """Abstract base class for different types of items with an owner, title, created and updated timestamps."""

    owner = models.ForeignKey(
        User, related_name="%(class)s_related", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """meta class."""

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


# """
# # The new functionality added with the below course model
#
# class Category(models.Model):
# #    Represents a category with an ID, name, description, created by user, updated timestamp, and state.
#
#     id = models.AutoField(primary_key=True, help_text="Primary key")
#     name = models.CharField(max_length=255, null=False, help_text="Name of the category")
#     description = models.TextField(blank=True, null=True, help_text="Description of the category")
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_categories",
#       help_text="User who created the category")
#     updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp of the last update")
#     state = models.BooleanField(default=True, help_text="State of the category (active/inactive)")
#
#     def __str__(self):
# #        Returns the string representation of the Category.
#         return self.name
#
#
# class Course(models.Model):
# #    Represents a course with an ID.
#
#     id = models.AutoField(primary_key=True, help_text="Primary key")
#     title = models.CharField(max_length=255, null=False, help_text="Title of the course")
#     slug = models.SlugField(max_length=255, unique=True, help_text="Unique slug for the course")
#     description = models.TextField(blank=True, null=True, help_text="Description of the course")
#     price = models.DecimalField(max_digits=10, decimal_places=2, null=True,
#     blank=True, help_text="Price of the course")
#     currency = models.CharField(max_length=10, null=True, blank=True, help_text="Currency of the price")
#     is_paid = models.BooleanField(default=False, help_text="Indicates if the course is paid or not")
#     categories = models.ManyToManyField(Category, related_name="courses",
#     help_text="Categories this course belongs to")
#     created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp of creation")
#     enroll_start_date = models.DateField(null=True, blank=True, help_text="Enrollment start date")
#     enroll_end_date = models.DateField(null=True, blank=True, help_text="Enrollment end date")
#     completion_days = models.IntegerField(null=True, blank=True, help_text="Number of days to complete the course")
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_courses",
#     help_text="User who created the course")
#     updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp of the last update")
#     state = models.BooleanField(default=True, help_text="State of the course (active/inactive)")
#
#     def __str__(self):
# #        Returns the string representation of the Course.
#         return self.title
# """


class Enrollment(models.Model):
    """Represents an enrollment with an ID."""

    id = models.AutoField(primary_key=True, help_text="Primary key")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="enrollments",
        help_text="User who enrolled in the course",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments",
        help_text="Course this enrollment belongs to",
    )
    enrollment_date = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp of enrollment"
    )
    target_end_date = models.DateField(
        null=True, blank=True, help_text="Target end date for the enrollment"
    )
    is_completed = models.BooleanField(
        default=False, help_text="Indicates if the enrollment is completed"
    )
    completion_date = models.DateField(
        null=True, blank=True, help_text="Date of completion"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_enrollments",
        help_text="User who created the enrollment",
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp of the last update"
    )
    state = models.BooleanField(
        default=True, help_text="State of the enrollment (active/inactive)"
    )

    def __str__(self):
        """Returns the string representation of the Enrollment."""
        return f"Enrollment of {self.user.username} in {self.course.title}"


class Certificate(models.Model):
    """Represents a certificate with an ID."""

    id = models.AutoField(primary_key=True, help_text="Primary key")
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="certificates",
        help_text="Course this certificate belongs to",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="certificates",
        help_text="User who received the certificate",
    )
    issue_date = models.DateField(help_text="Issue date of the certificate")
    eol_date = models.DateField(
        null=True, blank=True, help_text="End of life date of the certificate"
    )
    certificate_url = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="URL of the certificate",
    )
    state = models.BooleanField(
        default=True, help_text="State of the certificate (active/inactive)"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_certificates",
        help_text="User who created the certificate",
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp of the last update"
    )

    def __str__(self):
        """Returns the string representation of the Certificate."""
        return f"Certificate for {self.user.username} in {self.course.title}"


class CertificateMaster(models.Model):
    """Represents a certificate master template with an ID."""

    id = models.AutoField(primary_key=True, help_text="Primary key")
    title = models.CharField(
        max_length=255, null=False, help_text="Title of the certificate"
    )
    design = models.TextField(
        blank=True, null=True, help_text="Design of the certificate"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_certificate_masters",
        help_text="User who created the certificate master",
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp of the last update"
    )
    state = models.BooleanField(
        default=True,
        help_text="State of the certificate master (active/inactive)",
    )

    def __str__(self):
        """Returns the string representation of the CertificateMaster."""
        return str(self.title)
