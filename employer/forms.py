from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from employer.models import Vacancy


class VacancyCreateForm(forms.ModelForm):
    experience = forms.ChoiceField(
        choices=Vacancy.EXPERIENCE_CHOICE,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    employment_type = forms.ChoiceField(
        choices=Vacancy.EMPLOYMENT_TYPE_CHOICE,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    is_published = forms.RadioSelect()

    class Meta:
        model = Vacancy
        fields = (
            "position",
            "experience",
            "city",
            "salary_from",
            "salary_to",
            "employment_type",
            "is_published",
        )

        widgets = {
            "position": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Position"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "City"}
            ),
        }
