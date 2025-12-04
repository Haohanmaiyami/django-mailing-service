from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import (
    RegisterView,
    VerifyEmailView, UserUpdateView, ProfileView,
)
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "login/",
        LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "verify/<uidb64>/<token>/",
        VerifyEmailView.as_view(),
        name="verify_email",
    ),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            success_url=reverse_lazy("users:password_reset_done"),
            email_template_name="registration/password_reset_email.html",
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("profile/edit/", UserUpdateView.as_view(), name="profile_edit"),
    path("profile/", ProfileView.as_view(), name="profile"),
]
