from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .forms import LoginForm
from .views import RegisterView, UserLoginView, UserLogoutView, CustomLoginView
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path("login/", LoginView.as_view(template_name="users/login.html", authentication_form=LoginForm), name="login"),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('confirm/<uidb64>/<token>/', views.confirm_email, name='confirm_email'),
]
