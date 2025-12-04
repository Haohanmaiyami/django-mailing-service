from django.core.management.base import BaseCommand
from django.utils import timezone
from mailing.models import Mailing, Attempt
from django.core.mail import send_mail


class Command(BaseCommand):
    help = "Send active mailings to clients"

    def handle(self, *args, **kwargs):
        now = timezone.now()
        mailings = Mailing.objects.filter(
            status="Запущена", start_time__lte=now, end_time__gte=now
        )

        for mailing in mailings:
            for client in mailing.clients.all():
                try:
                    send_mail(
                        subject=mailing.message.subject,
                        message=mailing.message.body,
                        from_email=None,
                        recipient_list=[client.email],
                        fail_silently=False,
                    )
                    status = "Успешно"
                    server_response = "200 OK"
                except Exception as e:
                    status = "Не успешно"
                    server_response = str(e)

                Attempt.objects.create(
                    mailing=mailing,
                    datetime=timezone.now(),
                    status=status,
                    server_response=server_response,
                )

        self.stdout.write(self.style.SUCCESS("Рассылки успешно выполнены."))
