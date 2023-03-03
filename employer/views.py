from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    CreateView,
    DeleteView,
)

from employer.mixins import EmployerLoginRequiredMixin
from employer.models import Vacancy
from employer.forms import (
    VacancyCreateForm,
)


class VacancyListView(EmployerLoginRequiredMixin, ListView):
    models = Vacancy
    template_name = "employer/vacancies.html"
    context_object_name = "vacancies"

    queryset = Vacancy.objects.filter(is_published=True)


class MyVacancyListView(VacancyListView):
    def get_queryset(self):
        return super().get_queryset().filter(employer=self.request.user)


class VacancyDetailView(EmployerLoginRequiredMixin, DetailView):
    model = Vacancy
    template_name = "employer/vacancy-detail.html"


class VacancyUpdateView(EmployerLoginRequiredMixin, UpdateView):
    model = Vacancy
    form_class = VacancyCreateForm
    template_name = "employer/vacancy-edit.html"


class VacancyCreateView(EmployerLoginRequiredMixin, CreateView):
    model = Vacancy
    form_class = VacancyCreateForm
    template_name = "employer/vacancy-create.html"

    def form_valid(self, form):
        form.instance.employer = self.request.user
        return super(VacancyCreateView, self).form_valid(form)


class VacancyDeleteView(EmployerLoginRequiredMixin, DeleteView):
    model = Vacancy
    success_url = reverse_lazy("employer:vacancies")
    template_name = "employer/vacancy_confirm_delete.html"
