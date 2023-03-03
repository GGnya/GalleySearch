from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

from applicant.forms import CreateResumeForm
from applicant.mixins import ApplicantLoginRequiredMixin
from applicant.models import Resume


class ResumeListView(ApplicantLoginRequiredMixin, ListView):
    model = Resume
    template_name = "applicant/resumes.html"
    context_object_name = "resumes"

    queryset = Resume.objects.filter(is_published=True)


class MyResumesListView(ResumeListView):
    def get_queryset(self):
        return super().get_queryset().filter(applicant=self.request.user)


class ResumeDetailView(ApplicantLoginRequiredMixin, DetailView):
    model = Resume
    template_name = "applicant/resume-detail.html"


class ResumeCreateView(ApplicantLoginRequiredMixin, CreateView):
    model = Resume
    form_class = CreateResumeForm
    template_name = "applicant/resume-create.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["initial"] = {"email": self.request.user.email}
        return kwargs

    def form_valid(self, form):
        form.instance.applicant = self.request.user
        return super().form_valid(form)


class ResumeUpdateView(ApplicantLoginRequiredMixin, UpdateView):
    model = Resume
    form_class = CreateResumeForm
    template_name = "applicant/resume-edit.html"


class ResumeDeleteView(ApplicantLoginRequiredMixin, DeleteView):
    model = Resume
    success_url = reverse_lazy("applicant:resumes")
    template_name = "applicant/resume_confirm_delete.html"
