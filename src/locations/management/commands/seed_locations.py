from django.core.management.base import BaseCommand
from faker import Faker
import random

from locations.models import Region, Country, State, City
from listings.models import Listing
from users.models import User

fake = Faker()


class Command(BaseCommand):
    help = "Создаёт регионы, страны, штаты, города и объявления с Faker"

    def handle(self, *args, **kwargs):
        self.stdout.write("🌍 Начинаем генерацию географических данных...")

        # Очистим только локации и связанные объявления
        Listing.objects.all().delete()
        City.objects.all().delete()
        State.objects.all().delete()
        Country.objects.all().delete()
        Region.objects.all().delete()

        regions_data = {
            "Европа": {
                "Германия": ["Бавария", "Саксония", "Бранденбург"],
                "Франция": ["Иль-де-Франс", "Прованс", "Нормандия"],
                "Польша": ["Мазовецкое", "Малопольское", "Поморское"]
            },
            "США": {
                "США": ["Калифорния", "Техас", "Нью-Йорк", "Флорида"]
            },
            "Азия": {
                "Япония": ["Токио", "Осака", "Хоккайдо"],
                "Китай": ["Гуандун", "Пекин", "Шанхай"]
            }
        }

        landlords = list(User.objects.filter(is_staff=False))
        if not landlords:
            self.stdout.write(self.style.WARNING("⚠️ Нет пользователей! Создай хотя бы одного пользователя."))
            return

        for region_name, countries in regions_data.items():
            region = Region.objects.create(name=region_name)
            self.stdout.write(f"🗺️ Регион: {region_name}")

            for country_name, states in countries.items():
                country = Country.objects.create(name=country_name, region=region)
                self.stdout.write(f"  🌎 Страна: {country_name}")

                for state_name in states:
                    state = State.objects.create(name=state_name, country=country)
                    self.stdout.write(f"    🏙️ Штат/Область: {state_name}")

                    # Создаём города
                    for _ in range(random.randint(2, 4)):
                        city_name = fake.city()
                        city = City.objects.create(name=city_name, state=state)
                        self.stdout.write(f"      🏡 Город: {city_name}")

                        # Создаём 20 объявлений для каждого города
                        for _ in range(20):
                            owner = random.choice(landlords)
                            Listing.objects.create(
                                owner=owner,
                                title=fake.sentence(nb_words=4),
                                description=fake.paragraph(nb_sentences=3),
                                price=round(random.uniform(50, 1000), 2),
                                price_currency=random.choice(["EUR", "USD", "GBP", "PLN"]),
                                is_available=random.choice([True, True, True, False]),
                                country=country.name,
                                city=city,
                                street=fake.street_name(),
                                house_number=str(random.randint(1, 150)),
                            )

        self.stdout.write(self.style.SUCCESS("✅ База успешно заполнена географическими данными!"))
