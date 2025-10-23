from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.exceptions import ValidationError
from faker import Faker
import random
from datetime import timedelta, date

from users.models import User
from listings.models import Listing
from locations.models import Region, Country, State, City
from bookings.models import Booking
from reviews.models import Review

fake = Faker('de_DE')


class Command(BaseCommand):
    help = "Полное заполнение базы тестовыми данными"

    def handle(self, *args, **options):
        self.stdout.write("🚀 Начинаем наполнение базы...")

        # ---- USERS ----
        User.objects.all().delete()

        hosts = [
            User.objects.create_user(
                username=f"host_{i}",
                email=f"host_{i}@example.com",
                password="1234"
            )
            for i in range(80)
        ]

        tenants = [
            User.objects.create_user(
                username=f"tenant_{i}",
                email=f"tenant_{i}@example.com",
                password="1234"
            )
            for i in range(50)
        ]

        guests = [
            User.objects.create_user(
                username=f"guest_{i}",
                email=f"guest_{i}@example.com",
                password="1234"
            )
            for i in range(10)
        ]

        self.stdout.write(
            f"✅ Пользователи: {len(hosts)} арендодателей, {len(tenants)} арендаторов, {len(guests)} гостей"
        )

        # ---- LOCATIONS ----
        Booking.objects.all().delete()
        Review.objects.all().delete()
        Listing.objects.all().delete()
        City.objects.all().delete()
        State.objects.all().delete()
        Country.objects.all().delete()
        Region.objects.all().delete()

        region = Region.objects.create(name="Европа")
        country = Country.objects.create(name="Германия", region=region)
        state = State.objects.create(name="Бавария", country=country)

        cities = []
        city_names = set()
        while len(cities) < 20:
            name = fake.city()
            if name in city_names:
                continue
            city_names.add(name)
            city = City.objects.create(name=name, state=state)
            cities.append(city)

        self.stdout.write(f"✅ Создано {len(cities)} городов")

        # ---- LISTINGS ----
        listings = []
        for _ in range(200):
            city = random.choice(cities)
            owner = random.choice(hosts)
            listing = Listing.objects.create(
                title=fake.sentence(nb_words=4),
                description=fake.text(max_nb_chars=200),
                price=random.randint(30, 500),
                city=city,
                owner=owner,
                country="Германия",
                street=fake.street_name(),
                house_number=str(random.randint(1, 100)),
                apartment_number=str(random.randint(1, 50)),
            )
            listings.append(listing)

        self.stdout.write(f"✅ Создано {len(listings)} объявлений")

        # ---- BOOKINGS ----
        bookings = []
        today = date.today()

        for _ in range(300):
            tenant = random.choice(tenants)
            listing = random.choice(listings)
            start_date = today + timedelta(days=random.randint(1, 60))
            end_date = start_date + timedelta(days=random.randint(2, 10))
            status = random.choice(["approved", "rejected", "pending", "canceled"])

            try:
                booking = Booking.objects.create(
                    tenant=tenant,
                    listing=listing,
                    start_date=start_date,
                    end_date=end_date,
                    status=status,
                )
                bookings.append(booking)
            except ValidationError:
                continue  # пропускаем некорректные даты

        self.stdout.write(f"✅ Создано {len(bookings)} бронирований (без пересечений)")

        # ---- REVIEWS ----
        completed = [b for b in bookings if b.status == "approved"]

        for booking in random.sample(completed, k=min(50, len(completed))):
            Review.objects.create(
                booking=booking,
                listing=booking.listing,
                user=booking.tenant,  # исправлено с booking.user
                rating=random.randint(3, 5),
                comment=fake.sentence(nb_words=12),
            )

        self.stdout.write(f"✅ Создано отзывов: {min(50, len(completed))}")
        self.stdout.write(self.style.SUCCESS("🎉 База успешно заполнена тестовыми данными!"))
