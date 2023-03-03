from django import forms
from djmoney.forms import MoneyField, MoneyWidget

from applicant.models import Resume


class CreateResumeForm(forms.ModelForm):
    gender = forms.ChoiceField(
        choices=Resume.GENDER_CHOICE,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    salary_to = MoneyField(
        default_currency="RUB",
        widget=MoneyWidget(
            amount_widget=forms.TextInput(
                attrs={"class": "form-control-mg3", "placeholder": "Salary"}
            )
        ),
    )
    is_published = forms.RadioSelect()

    class Meta:
        model = Resume
        fields = (
            "first_name",
            "last_name",
            "birthday",
            "gender",
            "position",
            "city",
            "email",
            "salary_to",
            "is_published",
        )

        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "First name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Last name"}
            ),
            "birthday": forms.DateInput(
                attrs={"class": "form-control", "placeholder": "YYYY-MM-DD"}
            ),
            "position": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Position"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "City"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
        }
