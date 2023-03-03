from django.urls import path

from applicant.views import (
    ResumeListView,
    ResumeDetailView,
    ResumeCreateView,
    ResumeUpdateView,
    ResumeDeleteView,
    MyResumesListView,
)

app_name = "applicant"

urlpatterns = [
    path("resumes/", ResumeListView.as_view(), name="resumes"),
    path("resume/<int:pk>/", ResumeDetailView.as_view(), name="resume-detail"),
    path("resume/create-resume/", ResumeCreateView.as_view(), name="create-resume"),
    path("resume/<int:pk>/edit/", ResumeUpdateView.as_view(), name="edit-resume"),
    path("resume/<int:pk>/delete/", ResumeDeleteView.as_view(), name="delete-resume"),
    path("my-resumes/", MyResumesListView.as_view(), name="my-resumes"),
]
