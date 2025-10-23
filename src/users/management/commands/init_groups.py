from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = "Создаёт базовые группы пользователей и назначает права"

    def handle(self, *args, **options):
        # Создаём группы
        tenant_group, _ = Group.objects.get_or_create(name="Tenant")
        landlord_group, _ = Group.objects.get_or_create(name="Landlord")

        # Пример: добавляем права арендодателю
        landlord_perms = Permission.objects.filter(
            codename__in=[
                "add_listing", "change_listing", "delete_listing", "view_listing",
                "view_booking"
            ]
        )
        landlord_group.permissions.set(landlord_perms)

        # Пример: арендатор может только просматривать и бронировать
        tenant_perms = Permission.objects.filter(
            codename__in=[
                "view_listing", "add_booking", "view_booking"
            ]
        )
        tenant_group.permissions.set(tenant_perms)

        self.stdout.write(self.style.SUCCESS("✅ Группы Tenant и Landlord инициализированы"))
