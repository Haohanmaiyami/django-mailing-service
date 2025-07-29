from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import RegisterForm, LoginForm
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # пользователь не активен до подтверждения
        user.save()
        # Генерируем токен и UID для подтверждения
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activate_url = self.request.build_absolute_uri(
            reverse('users:confirm_email', args=[uid, token])
        )
        # Отправляем email с ссылкой активации
        send_mail(
            "Подтверждение регистрации",
            f"Здравствуйте, {user.username}!\n\nПерейдите по ссылке, чтобы подтвердить email: {activate_url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        messages.info(self.request, "На вашу почту отправлена ссылка для подтверждения регистрации.")
        return redirect('users:login')

class UserRegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/register.html'

class UserLoginView(LoginView):
    template_name = 'users/login.html'

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')

def confirm_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None
    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Email успешно подтверждён! Теперь вы можете войти.")
    else:
        messages.error(request, "Ссылка для подтверждения недействительна или устарела.")
    return redirect('users:login')

class CustomLoginView(LoginView):
    authentication_form = LoginForm