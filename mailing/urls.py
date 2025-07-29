from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views
from .views import IndexView, MailingListView, MailingCreateView, MailingUpdateView, MailingDeleteView, MessageListView, \
    ClientListView, AttemptListView, SendMailingView, ClientCreateView, MessageCreateView

app_name = 'mailing'


class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('mailings/', MailingListView.as_view(), name='list'),
    path('mailings/create/', MailingCreateView.as_view(), name='create'),
    path('mailings/<int:pk>/update/', MailingUpdateView.as_view(), name='update'),
    path('mailings/<int:pk>/delete/', MailingDeleteView.as_view(), name='delete'),
    path('mailings/<int:pk>/send/', SendMailingView.as_view(), name='send'),
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('logs/', AttemptListView.as_view(), name='log_list'),
    path('clients/<int:pk>/update/', views.ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/delete/', views.ClientDeleteView.as_view(), name='client_delete'),
    path('accounts/logout/', csrf_exempt(CustomLogoutView.as_view()), name='logout'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
]
