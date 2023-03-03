from django.urls import path

from account.views import (
    employer_register_view,
    employer_register_company_view,
    UserLoginView,
    main_page_view,
    logout_view,
    applicant_register_view,
    ProfileView,
    profile_edit_view,
)

app_name = "account"

urlpatterns = [
    path("", main_page_view, name="main-page"),
    path("register-employer/", employer_register_view, name="employer-register"),
    path(
        "register-company/",
        employer_register_company_view,
        name="employer-register-company",
    ),
    path("register-applicant/", applicant_register_view, name="applicant-register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("accounts/profile/", ProfileView.as_view(), name="self-profile"),
    path("accounts/profile/<int:pk>/", ProfileView.as_view(), name="profile"),
    path("accounts/profile/edit/", profile_edit_view, name="profile-edit"),
]
