from django import forms
from .models import StudentCompetition

class StudentCompetitionForm(forms.ModelForm):
    class Meta:
        model = StudentCompetition
        fields = ['user', 'status']

    status = forms.ChoiceField(choices=[(1, 'Active'), (0, 'Inactive')], widget=forms.RadioSelect)
