from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView

from account.forms import (
    EmployerRegisterCompanyForm,
    EmployerEditForm,
    EmployerProfileEditForm,
    EmployerRegisterForm,
    ApplicantRegisterForm,
    UserLoginForm,
    ApplicantEditForm,
    ApplicantProfileEditForm,
)
from account.models import Employer, EmployerProfile, Applicant, User, ApplicantProfile


class ProfileView(DetailView):
    model = User
    template_name = "account/profile.html"
    context_object_name = "profile"

    def get(self, request, *args, **kwargs):
        if not self.kwargs.get("pk"):
            if not self.request.user.is_authenticated:
                return redirect("account:login")
            self.kwargs["pk"] = request.user.pk
        profile = get_object_or_404(self.model, pk=self.kwargs.get("pk"))

        if self.request.user.role == "APPLICANT":
            extra_context = ApplicantProfile.objects.filter(user=profile)
        elif self.request.user.role == "EMPLOYER":
            extra_context = EmployerProfile.objects.filter(user=profile)

        context = {
            "profile": profile,
        }
        if extra_context:
            context["extra_profile"] = extra_context.get()
        return render(request, template_name=self.template_name, context=context)


def employer_register_view(request):
    if request.user.is_authenticated:
        return redirect("applicant:resumes")
    form = EmployerRegisterForm
    if request.method == "POST":
        form = EmployerRegisterForm(request.POST)
        if form.is_valid():
            employer = form.save()
            login(request, employer)
            messages.info(
                request, "Thanks, one more step to complete the registration."
            )
            return HttpResponseRedirect(reverse("account:employer-register-company"))
        messages.error(request, form.errors)
    context = {"form": form}
    return render(request, "account/register.html", context)


def employer_register_company_view(request):
    form = EmployerRegisterCompanyForm
    if request.method == "POST":
        obj = get_object_or_404(EmployerProfile, user_id=request.user.pk)
        form = EmployerRegisterCompanyForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.info(request, "Thanks for registration, now u can do what u want.")
            return HttpResponseRedirect(reverse("applicant:resumes"))
        messages.error(request, form.errors)
    context = {"form": form}
    return render(request, "account/register.html", context)


def applicant_register_view(request):
    if request.user.is_authenticated:
        return redirect("employer:vacancies")
    form = ApplicantRegisterForm
    if request.method == "POST":
        form = ApplicantRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.info(request, "Thanks for registration, now u can do what u want.")
            return HttpResponseRedirect(reverse("employer:vacancies"))
        messages.error(request, form.errors)
    context = {"form": form}
    return render(request, "account/register.html", context)


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "account/login.html"
    success_url = "account:main-page"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role == "APPLICANT":
                return redirect("employer:vacancies")
            elif request.user.role == "EMPLOYER":
                return redirect("applicant:resumes")
            return redirect("/admin")
        return super().dispatch(request, *args, **kwargs)


@login_required(login_url="account:login")
def profile_edit_view(request):
    if request.user.role == "EMPLOYER":
        klass_user = Employer
        klass_profile = EmployerProfile
        form_ = EmployerEditForm
        form2_ = EmployerProfileEditForm
    if request.user.role == "APPLICANT":
        klass_user = Applicant
        klass_profile = ApplicantProfile
        form_ = ApplicantEditForm
        form2_ = ApplicantProfileEditForm

    user = get_object_or_404(klass=klass_user, pk=request.user.pk)
    form = form_(instance=user)

    user_profile = get_object_or_404(klass=klass_profile, user_id=request.user.pk)
    form2 = form2_(instance=user_profile)

    if request.method == "POST":
        form = form_(request.POST, instance=user)
        form2 = form2_(request.POST, instance=user_profile)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            messages.info(request, "Profile updated successfully")
            return HttpResponseRedirect(reverse("account:self-profile"))
    context = {"form": form, "form2": form2}
    return render(request, "account/profile-edit.html", context)


def main_page_view(request):
    if request.user.is_authenticated:
        if request.user.role == "EMPLOYER":
            return redirect("applicant:resumes", permanent=True)
        elif request.user.role == "APPLICANT":
            return redirect("employer:vacancies", permanent=True)
    return render(request, "account/index.html")


@login_required(login_url="account:login")
def logout_view(request):
    logout(request)
    return redirect("account:login")
