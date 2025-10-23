from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.utils import timezone
from faker import Faker
import random
import logging

from users.models import User
from listings.models import Listing
from bookings.models import Booking
from reviews.models import Review
from locations.models import City, State, Country, Region

logger = logging.getLogger(__name__)
fake = Faker("de_DE")  # немецкая локаль для реалистичных данных


class Command(BaseCommand):
    help = "Заполняет базу данных тестовыми пользователями, локациями, объявлениями, бронированиями и отзывами."

    def handle(self, *args, **options):
        logger.info("🔹 Начало заполнения базы данных...")

        # === Группы пользователей ===
        landlord_group, _ = Group.objects.get_or_create(name="Landlord")
        guest_group, _ = Group.objects.get_or_create(name="Guest")

        # === Создание пользователей ===
        users = []
        for _ in range(20):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password="password123",
            )
            user_group = random.choice([landlord_group, guest_group])
            user.groups.add(user_group)
            users.append(user)
            logger.info(f"[USERS] 👤 User '{user.username}' added to group '{user_group.name}'")

        self.stdout.write(self.style.SUCCESS("✅ Пользователи созданы и распределены по группам!"))

        # === Регионы и страны ===
        region, _ = Region.objects.get_or_create(name="Europe")
        country, _ = Country.objects.get_or_create(name="Germany", region=region)
        self.stdout.write(self.style.SUCCESS(f"🌍 Страна создана: {country.name}"))

        # === Штаты ===
        states = []
        state_names = [
            "Bayern",
            "Berlin",
            "Nordrhein-Westfalen",
            "Hessen",
            "Sachsen",
            "Baden-Württemberg",
        ]
        for name in state_names:
            state, _ = State.objects.get_or_create(name=name, country=country)
            states.append(state)
        self.stdout.write(self.style.SUCCESS(f"🏞️ Штаты созданы: {len(states)} шт."))

        # === Города ===
        cities = []
        for _ in range(10):
            city_name = fake.city()
            state = random.choice(states)
            city, _ = City.objects.get_or_create(name=city_name, state=state)
            cities.append(city)
        self.stdout.write(self.style.SUCCESS(f"🏙️ Города созданы: {len(cities)} шт."))

        # === Объявления ===
        listings = []
        for _ in range(30):
            owner = random.choice(users)
            if owner.groups.filter(name="Landlord").exists():
                city = random.choice(cities)
                listing = Listing.objects.create(
                    owner=owner,
                    title=fake.sentence(nb_words=3),
                    description=fake.text(max_nb_chars=200),
                    price=random.randint(50, 400),
                    city=city,
                    is_available=random.choice([True, True, False]),
                    created_at=timezone.now(),
                )
                listings.append(listing)
        self.stdout.write(self.style.SUCCESS(f"🏡 Объявлений создано: {len(listings)} шт."))

        # === Бронирования ===
        bookings = []
        guests = [u for u in users if u.groups.filter(name="Guest").exists()]

        for _ in range(40):
            guest = random.choice(guests)
            listing = random.choice(listings)
            start_date = timezone.now().date() + timezone.timedelta(days=random.randint(1, 10))
            end_date = start_date + timezone.timedelta(days=random.randint(2, 14))
            booking = Booking.objects.create(
                tenant=guest,  # ✅ заменено user → tenant
                listing=listing,
                start_date=start_date,
                end_date=end_date,
                status=random.choice(["pending", "approved", "canceled"]),
            )
            bookings.append(booking)
        self.stdout.write(self.style.SUCCESS(f"📅 Бронирований создано: {len(bookings)} шт."))

        # === Отзывы ===
        for _ in range(20):
            Review.objects.create(
                user=random.choice(users),
                listing=random.choice(listings),
                rating=random.randint(1, 5),
                comment=fake.sentence(),
                created_at=timezone.now(),
            )
        self.stdout.write(self.style.SUCCESS("⭐ Отзывы добавлены!"))

        logger.info("🎉 База данных успешно заполнена тестовыми данными!")
        self.stdout.write(self.style.SUCCESS("✅ Генерация завершена успешно!"))
