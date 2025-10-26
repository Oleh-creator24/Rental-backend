from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from listings.models import Listing
from bookings.models import Booking
from reviews.models import Review

class Command(BaseCommand):
    help = "Создаёт группы Tenant/Landlord и выдаёт им права"

    def handle(self, *args, **options):
        tenant_group, _ = Group.objects.get_or_create(name="Tenant")
        landlord_group, _ = Group.objects.get_or_create(name="Landlord")

        # Собираем стандартные модельные права
        def perms_for(model):
            ct = ContentType.objects.get_for_model(model)
            return Permission.objects.filter(content_type=ct)

        listing_perms = list(perms_for(Listing))
        booking_perms = list(perms_for(Booking))
        review_perms  = list(perms_for(Review))

        # Landlord: полные права на Listing, просмотр Booking/Review
        landlord_allow = [
            p for p in listing_perms  # все add/change/delete/view на объявления
        ] + [
            p for p in booking_perms if p.codename.startswith("view_")
        ] + [
            p for p in review_perms if p.codename.startswith("view_")
        ]

        # Tenant: просмотр Listings, создание/редактирование Booking/Review
        tenant_allow = [
            p for p in listing_perms if p.codename.startswith("view_")
        ] + [
            p for p in booking_perms if p.codename.split("_")[0] in ("add","change","view","delete")
        ] + [
            p for p in review_perms if p.codename.split("_")[0] in ("add","change","view","delete")
        ]

        landlord_group.permissions.set(landlord_allow)
        tenant_group.permissions.set(tenant_allow)

        self.stdout.write(self.style.SUCCESS("Группы и права обновлены"))
