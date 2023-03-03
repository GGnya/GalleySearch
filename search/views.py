from django.shortcuts import render
from django.views.generic import ListView

from applicant.models import Resume
from employer.models import Vacancy


# Create your views here.


class SearchResultListView(ListView):
    template_name = "search/search_results.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        resume_vacancy = self.request.GET.get("resume_vacancy")
        city = self.request.GET.get("city")
        salary_to = self.request.GET.get("salary_to")

        if resume_vacancy == "resume":
            object_list = Resume.objects.filter(is_published=True)
        else:
            object_list = Vacancy.objects.filter(is_published=True)
        if query:
            object_list = object_list.filter(position__icontains=query)
        if city:
            object_list = object_list.filter(city__icontains=city)
        if salary_to:
            object_list = object_list.filter(salary_to__lt=salary_to)

        if object_list:
            return object_list
