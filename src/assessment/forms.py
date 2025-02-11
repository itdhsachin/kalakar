from django import forms

from assessment.models import AssessmentUpload, StudentCompetition


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
