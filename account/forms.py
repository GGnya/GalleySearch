from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from account.models import EmployerProfile, Employer, Applicant, User, ApplicantProfile


class UserRegistrationFormMixin(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ("email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        model = self.Meta.model
        user = model.objects.filter(email__iexact=email)
        if user.exists():
            raise forms.ValidationError("A user with this email already exists")
        return email


class EmployerRegisterForm(UserRegistrationFormMixin, UserCreationForm):
    class Meta(UserRegistrationFormMixin.Meta):
        model = Employer


class ApplicantRegisterForm(UserRegistrationFormMixin, UserCreationForm):
    class Meta(UserRegistrationFormMixin.Meta):
        model = Applicant


class EmployerRegisterCompanyForm(forms.ModelForm):
    company_name = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = EmployerProfile
        fields = ("company_name",)

    def clean_company_name(self):
        company_name = self.cleaned_data.get("company_name")
        model = self.Meta.model
        obj = model.objects.filter(company_name__icontains=company_name)
        if obj.exists():
            raise forms.ValidationError("A company with this name already registered")
        return company_name


class UserLoginForm(AuthenticationForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput)

    class Meta:
        fields = ("email",)

    def clean_email(self):
        old_email = self.instance.email
        new_email = self.cleaned_data.get("email")
        model = self.Meta.model

        user = model.objects.filter(email__iexact=new_email)
        if user.exists() and old_email != new_email:
            raise forms.ValidationError("This email-address already taken")
        return new_email


class EmployerEditForm(UserEditForm, forms.ModelForm):
    class Meta(UserEditForm.Meta):
        model = Employer


class EmployerProfileEditForm(forms.ModelForm):
    company_name = forms.CharField(widget=forms.TextInput)
    some_info = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = EmployerProfile
        fields = ("company_name", "some_info")


class ApplicantProfileEditForm(forms.ModelForm):
    some_info = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = ApplicantProfile
        fields = ("some_info",)


class ApplicantEditForm(UserEditForm, forms.ModelForm):
    class Meta(UserEditForm.Meta):
        model = Applicant
