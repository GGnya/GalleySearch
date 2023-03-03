from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from djmoney.models.fields import MoneyField
from django.urls import reverse
from account.models import EmployerManager, User, Employer


class Vacancy(models.Model):
    EXPERIENCE_CHOICE = (
        ("WE", "Без опыта"),
        ("1+", "От 1 года"),
        ("2+", "От 2 лет"),
        ("3+", "От 3 лет"),
        ("5+", "Больше 5 лет"),
    )

    EMPLOYMENT_TYPE_CHOICE = (
        ("FT", "Полная занятость"),
        ("PT", "Частичная занятость"),
        ("IN", "Стажировка"),
        ("PW", "Проектная работа"),
    )

    employer = models.ForeignKey(
        Employer, on_delete=models.CASCADE, related_name="employer"
    )
    position = models.CharField(max_length=100, verbose_name="Должность")
    experience = models.CharField(
        max_length=2,
        verbose_name="Опыт работы",
        default="WE",
        choices=EXPERIENCE_CHOICE,
    )
    city = models.CharField(max_length=100, verbose_name="Город")
    salary_to = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="RUB",
        verbose_name="Зарплата до",
        blank=True,
    )
    salary_from = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="RUB",
        verbose_name="Зарплата от",
        blank=True,
    )
    employment_type = models.CharField(
        max_length=2,
        verbose_name="Тип занятости",
        default="FT",
        choices=EMPLOYMENT_TYPE_CHOICE,
    )
    is_published = models.BooleanField(verbose_name="Опубликовать", default=True)

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"

    def __str__(self):
        return self.position

    def get_absolute_url(self):
        return reverse("employer:vacancy-detail", kwargs={"pk": self.pk})

    def pretty_money(self):
        if self.salary_to and self.salary_from:
            return f"От {self.salary_from.amount} до {self.salary_to.amount} {self.salary_to_currency}"
        elif self.salary_to:
            return f"До {self.salary_to.amount} {self.salary_to_currency}"
        elif self.salary_from:
            f"От {self.salary_from.amount} {self.salary_from_currency}"
        return "Не указано"
