"""Models for the accounts app.

This module contains the models and custom manager for the accounts application,
including User and Student models.
"""

from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from PIL import Image

from accounts.validators import ASCIIUsernameValidator


class Session(models.Model):
    """Model representing a session.

    Attributes:
        session (str): The name of the session.
        is_current_session (bool): Indicates if the session is the current session.
        next_session_begins (date): The start date of the next session.
    """

    session = models.CharField(max_length=200, unique=True)
    is_current_session = models.BooleanField(
        default=False, blank=True, null=True
    )
    next_session_begins = models.DateField(blank=True, null=True)

    def __str__(self):
        """String representation of the session.

        Returns:
            str: The session name.
        """
        return f"{self.session}"


class CustomUserManager(UserManager):
    """Custom manager for User model.

    Methods:
        search(query): Search for users matching the query.
        get_student_count(): Get the count of student users.
        get_lecturer_count(): Get the count of lecturer users.
        get_superuser_count(): Get the count of superuser users.
    """

    def search(self, query=None):
        """Search for users matching the query.

        Args:
            query (str): The search query.

        Returns:
            QuerySet: The filtered queryset.
        """
        queryset = self.get_queryset()
        if query is not None:
            or_lookup = (
                Q(username__icontains=query)
                | Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(email__icontains=query)
            )
            queryset = queryset.filter(or_lookup).distinct()
        return queryset

    def get_student_count(self):
        """Get the count of student users.

        Returns:
            int: The count of student users.
        """
        return self.model.objects.filter(is_student=True).count()

    def get_lecturer_count(self):
        """Get the count of lecturer users.

        Returns:
            int: The count of lecturer users.
        """
        return self.model.objects.filter(is_lecturer=True).count()

    def get_superuser_count(self):
        """Get the count of superuser users.

        Returns:
            int: The count of superuser users.
        """
        return self.model.objects.filter(is_superuser=True).count()


GENDERS = ((_("M"), _("Male")), (_("F"), _("Female")))


class User(AbstractUser):
    """Model representing a user.

    Attributes:
        is_student (bool): Indicates if the user is a student.
        is_lecturer (bool): Indicates if the user is a lecturer.
        gender (str): The gender of the user.
        phone (str): The phone number of the user.
        address (str): The address of the user.
        picture (ImageField): The profile picture of the user.
        email (EmailField): The email address of the user.
        username_validator (ASCIIUsernameValidator): Validator for the username.
        objects (CustomUserManager): The custom manager for User model.

    Meta:
        ordering (tuple): Default ordering for the model.
    """

    is_student = models.BooleanField(default=False)
    is_lecturer = models.BooleanField(default=False)
    # full_name = models.CharField(max_length=255,blank=True)
    # birthday = models.DateField(null=True, blank=True)
    # gender = models.CharField(
    #     max_length=1, choices=GENDERS, blank=True, null=True
    # )
    phone = models.CharField(max_length=60, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    # address = models.CharField(max_length=60, blank=True, null=True)
    # picture = models.ImageField(
    #     upload_to="profile_pictures/%y/%m/%d/", default="default.png", null=True
    # )
    # education = models.CharField(max_length=255, blank=True)
    # taluka = models.CharField(max_length=100, blank=True)
    # District = models.CharField(max_length=100, blank=True)
    # state = models.CharField(max_length=100, blank=True)
    # pincode = models.CharField(max_length=6, blank=True)
    # ira_rangoli_reference = models.CharField(
    #     max_length=50,
    #     choices=[
    #         ("WhatsApp", "WhatsApp"),
    #         ("YouTube", "YouTube"),
    #         ("Instagram", "Instagram"),
    #         ("Friend", "Friend")
    #     ],
    #     blank=True,
    # )
    # hobbies = models.TextField(blank=True)
    username_validator = ASCIIUsernameValidator()

    objects = CustomUserManager()

    class Meta:
        """Meta options for the User model."""

        ordering = ("-date_joined",)

    
    def get_full_name(self):
        """Get the full name of the user.

        Returns:
            str: The full name of the user.
        """
        full_name = self.username
        if self.first_name and self.last_name:
            full_name = f"{self.first_name} {self.last_name}"
        return full_name

    def __str__(self):
        """String representation of the user.

        Returns:
            str: The username and full name of the user.
        """
        return f"{self.username} ({self.get_full_name})"

    def get_user_role(self):
        """Get the role of the user.

        Returns:
            str: The role of the user.
        """
        if self.is_superuser:
            return _("Admin")
        elif self.is_student:
            return _("Student")
        elif self.is_lecturer:
            return _("Lecturer")

    def get_picture(self):
        """Get the profile picture URL of the user.

        Returns:
            str: The URL of the profile picture.
        """
        try:
            return self.picture.url
        except AttributeError:
            no_picture = settings.MEDIA_URL + "default.png"
            return no_picture

    def get_absolute_url(self):
        """Get the absolute URL of the user profile.

        Returns:
            str: The URL of the user profile.
        """
        return reverse("profile_single", kwargs={"user_id": self.id})

    def save(self, *args, **kwargs):
        """Save the user model and resize the profile picture if necessary.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.picture.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.picture.path)
        except (FileNotFoundError, AttributeError):
            pass

    def delete(self, *args, **kwargs):
        """Delete the user model and the profile picture if it's not the default picture.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        if self.picture.url != settings.MEDIA_URL + "default.png":
            self.picture.delete()
        super().delete(*args, **kwargs)


class StudentManager(models.Manager):
    """Custom manager for Student model.

    Methods:
        search(query): Search for students matching the query.
    """

    def search(self, query=None): # pylint: disable=unused-argument
        """Search for students matching the query.

        Args:
            query (str): The search query.

        Returns:
            QuerySet: The filtered queryset.
        """
        qs = self.get_queryset()
        return qs


class Student(models.Model):
    """Model representing a student.

    Attributes:
        student (User): The user associated with the student.
        objects (StudentManager): The custom manager for Student model.

    Meta:
        ordering (tuple): Default ordering for the model.
    """

    student = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True)
    gender = models.CharField(
        max_length=1, choices=GENDERS, blank=True, null=True
    )
    birthday = models.DateField(null=True, blank=True)
    education = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=100, blank=True)
    taluka = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=6, blank=True)
    picture = models.ImageField(
        upload_to="profile_pictures/%y/%m/%d/", default="default.png", null=True
    )
    ira_rangoli_reference = models.CharField(
        max_length=50,
        choices=[
            ("WhatsApp", "WhatsApp"),
            ("YouTube", "YouTube"),
            ("Instagram", "Instagram"),
            ("Newspaper", "Newspaper"),
            ("Friend", "Friend"),
        ],
        blank=True,
    )
    hobbies = models.TextField(blank=True)

    objects = StudentManager()

    class Meta:
        """Meta options for the Student model."""

        ordering = ("-student__date_joined",)

    def __str__(self):
        """String representation of the student.

        Returns:
            str: The full name of the student.
        """
        return self.student.get_full_name

    def get_picture(self):
        """Get the profile picture URL of the user.

        Returns:
            str: The URL of the profile picture.
        """
        try:
            return self.picture.url
        except AttributeError:
            no_picture = settings.MEDIA_URL + "default.png"
            return no_picture

    @classmethod
    def get_gender_count(cls):
        """Get the count of students by gender.

        Returns:
            dict: A dictionary with the count of male and female students.
        """
        males_count = Student.objects.filter(student__gender="M").count()
        females_count = Student.objects.filter(student__gender="F").count()
        return {"M": males_count, "F": females_count}

    def get_absolute_url(self):
        """Get the absolute URL of the student profile.

        Returns:
            str: The URL of the student profile.
        """
        return reverse("profile_single", kwargs={"user_id": self.student.id})

    def delete(self, *args, **kwargs):
        """Delete the student model and the associated user.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.student.delete()
        super().delete(*args, **kwargs)


class TeacherManager(models.Manager):
    """Custom manager for Teacher model.

    Methods:
        search(query): Search for teachers matching the query.
    """

    def search(self, query=None): # pylint: disable=unused-argument
        """Search for teachers matching the query.

        Args:
            query (str): The search query.

        Returns:
            QuerySet: The filtered queryset.
        """
        qs = self.get_queryset()
        return qs


class Teacher(models.Model):
    """Model representing a teacher.

    Attributes:
        teacher (User): The user associated with the teacher.
        objects (TeacherManager): The custom manager for the Teacher model.

    Meta:
        ordering (tuple): Default ordering for the model.
    """

    teacher = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True)
    gender = models.CharField(
        max_length=1, choices=GENDERS, blank=True, null=True
    )
    birthday = models.DateField(null=True, blank=True)
    education = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=100, blank=True)
    taluka = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=6, blank=True)
    picture = models.ImageField(
        upload_to="profile_pictures/%y/%m/%d/", default="default.png", null=True
    )
    ira_rangoli_reference = models.CharField(
        max_length=50,
        choices=[
            ("WhatsApp", "WhatsApp"),
            ("YouTube", "YouTube"),
            ("Instagram", "Instagram"),
            ("Newspaper", "Newspaper"),
            ("Friend", "Friend"),
        ],
        blank=True,
    )
    hobbies = models.TextField(blank=True)
    last_rangoli_batch_completion_date = models.DateField(null=True, blank=True)
    level_completed = models.CharField(
        max_length=50,
        choices=[
            ("Basic", "Basic"),
            ("Special", "Special"),
            ("Advanced", "Advanced"),
            ("Professional", "Professional"),
            ("Extreme", "Extreme"),
        ],
        blank=True,
        null=True,
    )

    objects = TeacherManager()  # Custom Manager (if applicable)

    class Meta:
        """Meta options for the Teacher model."""

        ordering = ("-teacher__date_joined",)

    def __str__(self):
        """String representation of the teacher.

        Returns:
            str: The full name of the teacher.
        """
        return self.teacher.get_full_name

    @classmethod
    def get_gender_count(cls):
        """Get the count of teachers by gender.

        Returns:
            dict: A dictionary with the count of male and female teachers.
        """
        males_count = Teacher.objects.filter(teacher__gender="M").count()
        females_count = Teacher.objects.filter(teacher__gender="F").count()
        return {"M": males_count, "F": females_count}

    def get_picture(self):
        """Get the profile picture URL of the user.

        Returns:
            str: The URL of the profile picture.
        """
        try:
            return self.picture.url
        except AttributeError:
            no_picture = settings.MEDIA_URL + "default.png"
            return no_picture

    def get_absolute_url(self):
        """Get the absolute URL of the teacher profile.

        Returns:
            str: The URL of the teacher profile.
        """
        return reverse(
            "teacher_profile_single", kwargs={"user_id": self.teacher.id}
        )

    def delete(self, *args, **kwargs):
        """Delete the teacher model and the associated user.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.teacher.delete()
        super().delete(*args, **kwargs)
