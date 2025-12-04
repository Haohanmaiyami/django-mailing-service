from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy, reverse
from .forms import RegisterForm, LoginForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from .token import email_verification_token
from django.views import View
from .models import User

User = get_user_model()


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # пользователь не активен до подтверждения
        user.save()
        send_verification_email(self.request, user)
        messages.info(
            self.request,
            "На вашу почту отправлена ссылка для подтверждения регистрации.",
        )
        return redirect("users:login")


class UserLoginView(LoginView):
    template_name = "users/login.html"


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("users:login")


class VerifyEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and email_verification_token.check_token(user, token):
            user.is_verified = True
            user.is_active = True  # делаем активным после подтверждения
            user.save()
            messages.success(
                request, "Email подтверждён. Теперь вы можете войти."
            )
        else:
            messages.error(request, "Неверная или устаревшая ссылка.")

        return redirect("users:login")


def send_verification_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = email_verification_token.make_token(user)
    verify_url = request.build_absolute_uri(
        reverse("users:verify_email", kwargs={"uidb64": uid, "token": token})
    )
    subject = "Подтверждение регистрации"
    message = f"Перейдите по ссылке, чтобы подтвердить ваш email: {verify_url}"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


class CustomLoginView(LoginView):
    template_name = "users/login.html"
    authentication_form = LoginForm  # если ты используешь кастомную форму

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_verified:
            messages.error(self.request, "Подтвердите ваш email перед входом.")
            return redirect("users:login")
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['avatar', 'phone_number', 'country']
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"
