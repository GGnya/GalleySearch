from django.urls import path
from employer.views import (
    VacancyListView,
    VacancyDetailView,
    VacancyCreateView,
    VacancyUpdateView,
    VacancyDeleteView,
    MyVacancyListView,
)

app_name = "employer"

urlpatterns = [
    path("vacancies/", VacancyListView.as_view(), name="vacancies"),
    path("vacancy/<int:pk>/", VacancyDetailView.as_view(), name="vacancy-detail"),
    path("vacancy/create-vacancy", VacancyCreateView.as_view(), name="vacancy-create"),
    path("vacancy/<int:pk>/edit", VacancyUpdateView.as_view(), name="vacancy-edit"),
    path("vacancy/<int:pk>/delete", VacancyDeleteView.as_view(), name="vacancy-delete"),
    path("my-vacancies/", MyVacancyListView.as_view(), name="my-vacancies"),
]
