from django.core.mail import send_mail
from django.utils import timezone
from .models import Attempt
from django.conf import settings

def send_mailing(mailing):
    mailing.status = 'Запущена'
    mailing.save()
    all_sent = True
    error_message = ''
    for client in mailing.clients.all():
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[client.email],
                fail_silently=False,
            )
            Attempt.objects.create(mailing=mailing, status='Успешно', server_response='OK')
        except Exception as e:
            all_sent = False
            error_message = str(e)
            Attempt.objects.create(mailing=mailing, status='Не успешно', server_response=error_message)
    mailing.status = 'Завершена'
    mailing.save()
    if all_sent:
        return True, 'OK'
    return False, error_message