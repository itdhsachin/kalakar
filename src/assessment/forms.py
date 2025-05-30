from django import forms
import base64
from django.utils.html import format_html
from assessment.models import AssessmentUpload
from assessment.models import StudentCompetition

class StudentCompetitionForm(forms.ModelForm):
    """Form for managing student competition entries."""

    class Meta:
        """Metadata for StudentCompetitionForm."""

        model = StudentCompetition
        fields = ["user", "status"]

    status = forms.ChoiceField(
        choices=[(1, "Active"), (0, "Inactive")], widget=forms.RadioSelect
    )


class ReviewForm(forms.ModelForm):
    """Form for submitting reviews for assessment uploads."""

    class Meta:
        """Metadata for StudentCompetitionForm."""

        model = AssessmentUpload
        fields = ["review_score"]
        widgets = {
            "review_score": forms.RadioSelect(
                choices=[(i, str(i)) for i in range(1, 6)]
            )
        }

class AssessmentUploadForm(forms.ModelForm):
    """Custom form to display the binary image preview inside Django admin form."""

    class Meta:
        model = AssessmentUpload
        fields = "__all__"  # Show all fields in admin form

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # if self.instance and self.instance.work:
        #     image_base64 = base64.b64encode(self.instance.work).decode("utf-8")
        #     self.fields["work"].widget = forms.HiddenInput()  # Hide actual binary field
        #     self.fields["work"].help_text = format_html(
        #         '<img src="data:image/png;base64,{}" width="400" height="auto"/>', image_base64
        #     )