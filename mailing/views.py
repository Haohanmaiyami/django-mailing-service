from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from .forms import MailingForm
from .models import Mailing, Client, Message, Attempt
from django.core.cache import cache
from django.conf import settings
from django.contrib import messages
from .services import send_mailing

# @login_required
# def home(request):
#     total_mailings = Mailing.objects.count()
#     active_mailings = Mailing.objects.filter(status='Запущена').count()
#     unique_clients = Client.objects.values('email').distinct().count()
#     return render(request, 'mailing/index.html', {
#         'total_mailings': total_mailings,
#         'active_mailings': active_mailings,
#         'unique_clients': unique_clients,
#     })
# Список рассылок

class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailing/mailing_list.html"
    context_object_name = "mailings"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stats = {}
        for mailing in context["mailings"]:
            attempts = mailing.attempts.all()
            stats[mailing.id] = {
                "success": attempts.filter(status="Успешно").count(),
                "failed": attempts.filter(status="Не успешно").count(),
            }
        context["attempt_stats"] = stats
        return context


# Создание рассылки
class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ["email", "full_name", "comment"]
    template_name = "mailing/client_form.html"
    success_url = reverse_lazy("mailing:client_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ["subject", "body"]
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:message_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


# Обновление рассылки
class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm  # <--- тоже
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:list")


    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user:
            return HttpResponseForbidden(
                "Вы не можете редактировать этот объект."
            )
        return super().dispatch(request, *args, **kwargs)


# Удаление рассылки
class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailing/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailing:list")

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user:
            return HttpResponseForbidden("Вы не можете изменить эту рассылку.")
        return super().dispatch(request, *args, **kwargs)


class IndexView(TemplateView):
    template_name = "mailing/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if settings.CACHE_ENABLED:
            stats = cache.get("stats")
            if not stats:
                stats = {
                    "total_mailings": Mailing.objects.count(),
                    "active_mailings": Mailing.objects.filter(
                        status="Запущена"
                    ).count(),
                    "unique_clients": Client.objects.count(),
                }
                cache.set("stats", stats, 60)
        else:
            stats = {
                "total_mailings": Mailing.objects.count(),
                "active_mailings": Mailing.objects.filter(
                    status="Запущена"
                ).count(),
                "unique_clients": Client.objects.count(),
            }
        context.update(stats)
        return context


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "mailing/message_list.html"
    context_object_name = "messages"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "mailing/client_list.html"
    context_object_name = "clients"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Client.objects.all()
        return Client.objects.filter(owner=self.request.user)


class AttemptListView(LoginRequiredMixin, ListView):
    model = Attempt
    template_name = "mailing/attempt_list.html"
    context_object_name = "attempts"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Attempt.objects.all().order_by(
                "-datetime"
            )  # ⬅ сортировка по убыванию
        return Attempt.objects.filter(
            mailing__owner=self.request.user
        ).order_by("-datetime")


class SendMailingView(LoginRequiredMixin, View):
    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk, owner=request.user)
        success, response = send_mailing(mailing)
        if success:
            messages.success(request, "Письма успешно отправлены.")
        else:
            messages.error(request, f"Ошибка отправки: {response}")
        return redirect("mailing:list")


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = ["full_name", "email", "comment"]
    template_name = "mailing/client_form.html"
    success_url = reverse_lazy("mailing:client_list")

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().owner != request.user:
            return HttpResponseForbidden(
                "Недостаточно прав для редактирования этого клиента."
            )
        return super().dispatch(request, *args, **kwargs)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = "mailing/client_confirm_delete.html"
    success_url = reverse_lazy("mailing:client_list")

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().owner != request.user:
            return HttpResponseForbidden(
                "Недостаточно прав для удаления этого клиента."
            )
        return super().dispatch(request, *args, **kwargs)

class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ["subject", "body"]
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:message_list")

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().owner != request.user:
            return HttpResponseForbidden("Недостаточно прав для редактирования сообщения.")
        return super().dispatch(request, *args, **kwargs)

class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "mailing/message_confirm_delete.html"
    success_url = reverse_lazy("mailing:message_list")

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().owner != request.user:
            return HttpResponseForbidden("Недостаточно прав для удаления сообщения.")
        return super().dispatch(request, *args, **kwargs)