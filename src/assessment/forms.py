from django import forms
from .models import StudentCompetition, AssessmentUpload

class StudentCompetitionForm(forms.ModelForm):
    class Meta:
        model = StudentCompetition
        fields = ['user', 'status']

    status = forms.ChoiceField(choices=[(1, 'Active'), (0, 'Inactive')], widget=forms.RadioSelect)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = AssessmentUpload
        fields = ['review_score']
        widgets = {'review_score': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)])}
