from django import forms
import logging
from django.contrib.auth.forms import PasswordResetForm
from accounts.models import Student, Teacher, User,State,District
from django.core.exceptions import ValidationError

from courses.models import Course
logger = logging.getLogger(__name__)
class StudentForm(forms.ModelForm):
    """Form for Student profile updates."""

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control","readonly":"readonly"})
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control","readonly":"readonly"})
    )
    state = forms.ModelChoiceField(
        queryset=State.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-control", "id": "state-dropdown"})
    )
    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-control", "id": "district-dropdown"})
    )
    other_state = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "id": "other-state", "style": "display: none;"})
    )
    other_district = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "id": "other-district", "style": "display: none;"})
    )

    class Meta:
        """Meta options for the student form."""

        model = Student
        fields = [
            "full_name",
            "gender",
            "birthday",
            "education",
            "address",
            "taluka",
            "state",
            "other_state",
            "district",
            "other_district",
            "pincode",
            "picture",
            "ira_rangoli_reference",
            "hobbies",
        ]
        widgets = {
            "birthday": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "picture": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
        }

    def __init__(self, *args, **kwargs):
        """Initializer."""
        user = kwargs.pop("user", None)  # Get user instance if provided
        super().__init__(*args, **kwargs)
        if user:
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial = user.last_name
            self.fields["email"].initial = user.email
            self.fields["phone"].initial = user.phone

            # Make first_name readonly if already filled
            if user.first_name:
                self.fields["first_name"].widget.attrs["readonly"] = "readonly"

            # Make last_name readonly if already filled
            if user.last_name:
                self.fields["last_name"].widget.attrs["readonly"] = "readonly"

    
    
    def clean_picture(self):
        """Validate image size (max 2MB)."""
        picture = self.cleaned_data.get("picture")

        if picture:
            logger.info(f"Uploaded image size: {picture.size} bytes")
            max_size = 2 * 1024 * 1024 
        if picture.size > max_size:
            logger.warning("Image exceeds 2MB limit.")
            raise ValidationError("The uploaded image exceeds the 2MB limit. Please upload a smaller image.")

        return picture

class TeacherForm(forms.ModelForm):
    """Form for teacher profile updates."""

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control","readonly":"readonly"})
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control","readonly":"readonly"})
    )

    class Meta:
        """Meta options for the Teacher form."""

        model = Teacher
        fields = [
            "full_name",
            "gender",
            "birthday",
            "education",
            "address",
            "taluka",
            "district",
            "state",
            "pincode",
            "picture",
            "ira_rangoli_reference",
            "hobbies",
            "last_rangoli_batch_completion_date",
            "level_completed",
        ]
        widgets = {
            "birthday": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "last_rangoli_batch_completion_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "picture": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
        }

    def __init__(self, *args, **kwargs):
        """Intializer."""
        user = kwargs.pop("user", None)  # Get user instance if provided
        super().__init__(*args, **kwargs)
        if user:
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial = user.last_name
            self.fields["email"].initial = user.email
            self.fields["phone"].initial = user.phone


class CustomPasswordResetForm(PasswordResetForm):
    """Form for password reset functionality."""

    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Enter your email"}
        ),
    )

    def clean_email(self):
        """Validate that the provided email exists in the system.

        Returns:
            str: The cleaned email if it exists in the database.

        Raises:
            ValidationError: If the email does not exist.
        """
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "No user is associated with this email address."
            )
        return email

# class CourseEnrollForm(forms.Form):
#     """Form for enrolling in a course.

#     Attributes:
#         course (ModelChoiceField): A hidden field to select a course.
#     """

#     course = forms.ModelChoiceField(
#         queryset=Course.objects.all(), widget=forms.HiddenInput
#     )
