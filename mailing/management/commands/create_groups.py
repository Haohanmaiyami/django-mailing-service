from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from mailing.models import Mailing, Message, Client


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        group, _ = Group.objects.get_or_create(name="Менеджеры")
        for model in [Mailing, Message, Client]:
            for codename in ["add", "change", "delete", "view"]:
                permission = Permission.objects.get(
                    content_type__app_label="mailing",
                    codename=f"{codename}_{model._meta.model_name}",
                )
                group.permissions.add(permission)
        self.stdout.write("Группа Менеджеры создана.")
