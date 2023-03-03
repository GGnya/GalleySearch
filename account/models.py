from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_super_user(self, email, password, **other_fields):
        other_fields["is_staff"] = True
        return self.create_user(email, password, **other_fields)


class User(AbstractBaseUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        EMPLOYER = "EMPLOYER", "Employer"
        APPLICANT = "APPLICANT", "Applicant"

    email = models.EmailField(db_index=True, unique=True, verbose_name="Email")
    date_created = models.DateTimeField(verbose_name="Date created")
    date_updated = models.DateTimeField(verbose_name="Date updated")
    is_active = models.BooleanField(verbose_name="Active user", default=True)
    is_staff = models.BooleanField(verbose_name="Super user", default=False)
    role = models.CharField(verbose_name="Role", choices=Role.choices, max_length=15)

    base_role = Role.ADMIN
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # def __str__(self):
    #     return self.email

    def save(self, *args, **kwargs):
        if not self.pk:
            self.date_created = timezone.now()
            self.role = self.base_role
        self.date_updated = timezone.now()
        return super(User, self).save(*args, **kwargs)


class EmployerManager(CustomUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Role.EMPLOYER)


class Employer(User):
    base_role = User.Role.EMPLOYER
    employer = EmployerManager()

    class Meta:
        proxy = True


class EmployerProfile(models.Model):
    user = models.OneToOneField(Employer, on_delete=models.CASCADE)
    company_name = models.CharField(
        verbose_name="Company name", db_index=True, max_length=150
    )
    some_info = models.TextField(verbose_name="Info", max_length=500)

    def get_some_info(self):
        return self.some_info

    def get_company_name(self):
        return self.company_name


@receiver(post_save, sender=Employer)
def create_employer_profile(sender, instance, created, **kwargs):
    if created and instance.role == "EMPLOYER":
        EmployerProfile.objects.create(user=instance)


class ApplicantManager(CustomUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Role.APPLICANT)


class Applicant(User):
    base_role = User.Role.APPLICANT
    applicant = ApplicantManager()

    class Meta:
        proxy = True


class ApplicantProfile(models.Model):
    user = models.OneToOneField(Applicant, on_delete=models.CASCADE)
    some_info = models.TextField(verbose_name="Info", max_length=500)

    def get_some_info(self):
        return self.some_info


@receiver(post_save, sender=Applicant)
def create_employer_profile(sender, instance, created, **kwargs):
    if created and instance.role == "APPLICANT":
        ApplicantProfile.objects.create(user=instance)
