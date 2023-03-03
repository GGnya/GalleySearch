from django.db import models
from django.urls import reverse
from djmoney.models.fields import MoneyField

from account.models import Applicant


class Resume(models.Model):
    GENDER_CHOICE = (("M", "Male"), ("F", "Female"))
    applicant = models.ForeignKey(
        Applicant, on_delete=models.CASCADE, related_name="applicant"
    )
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    birthday = models.DateField(verbose_name="Дата рождения")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE, verbose_name="Пол")
    position = models.CharField(
        max_length=100, verbose_name="Желаемая должность", db_index=True
    )
    city = models.CharField(max_length=100, verbose_name="Город")
    email = models.EmailField(verbose_name="Почта для связи")
    salary_to = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="RUB",
        verbose_name="Заработная плата",
    )
    is_published = models.BooleanField(verbose_name="Опубликовать", default=True)

    class Meta:
        verbose_name = "Резюме"
        verbose_name_plural = "Резюме"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("applicant:resume-detail", kwargs={"pk": self.pk})

    def pretty_money(self):
        return f"{self.salary_to.amount} {self.salary_to_currency}"
