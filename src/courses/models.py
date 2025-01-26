"""Course database models."""

from django.contrib.auth.models import User
from django.db import models


class Subject(models.Model):
    """Represents a subject with a title and slug."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        """Metaclass."""

        ordering = ["title"]

    def __str__(self):
        """Returns the string representation of the Subject."""
        return str(self.title)


class Course(models.Model):
    """Represents a course with an ID."""

    id = models.AutoField(primary_key=True, help_text="Primary key")
    title = models.CharField(
        max_length=255, null=False, help_text="Title of the course"
    )
    subject = models.ForeignKey(
        Subject, related_name="courses", on_delete=models.CASCADE
    )
    slug = models.SlugField(
        max_length=255, unique=True, help_text="Unique slug for the course"
    )
    description = models.TextField(
        blank=True, null=True, help_text="Description of the course"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Price of the course",
    )
    currency = models.CharField(
        max_length=10, null=True, blank=True, help_text="Currency of the price"
    )
    is_paid = models.BooleanField(
        default=False, help_text="Indicates if the course is paid or not"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp of creation"
    )
    enroll_start_date = models.DateField(
        null=True, blank=True, help_text="Enrollment start date"
    )
    enroll_end_date = models.DateField(
        null=True, blank=True, help_text="Enrollment end date"
    )
    completion_days = models.IntegerField(
        null=True, blank=True, help_text="Number of days to complete the course"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_courses",
        help_text="User who created the course",
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp of the last update"
    )
    state = models.BooleanField(
        default=True, help_text="State of the course (active/inactive)"
    )

    class Meta:
        """Metaclass."""

        ordering = ["-created_at"]

    def __str__(self):
        """Returns the string representation of the Course."""
        return str(self.title)


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
