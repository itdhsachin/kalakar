from django import forms
from .models import GENDERS, Student, Teacher, User
from django.contrib.auth.forms import PasswordResetForm

class StudentForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Student
        fields = [
            "full_name", "gender", "birthday", "education", "address",
            "taluka", "district", "state", "pincode", "picture",
            "ira_rangoli_reference", "hobbies"
        ]
        widgets = {
            "birthday": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "picture": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get user instance if provided
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            self.fields['phone'].initial = user.phone


class TeacherForm(forms.ModelForm):
    """Form for Teacher."""
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Teacher
        fields = [
            "full_name", "gender", "birthday", "education", "address",
            "taluka", "district", "state", "pincode", "picture",
            "ira_rangoli_reference", "hobbies", "last_rangoli_batch_completion_date", "level_completed"
        ]
        widgets = {
            "birthday": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "last_rangoli_batch_completion_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "picture": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get user instance if provided
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            self.fields['phone'].initial = user.phone

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter your email"}),
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No user is associated with this email address.")
        return email