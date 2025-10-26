import os
import sys
import django
import random
import uuid
from faker import Faker

# === Настройка окружения ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.config.settings")
django.setup()

# === Импорты моделей ===
from django.contrib.auth.models import Group
from listings.models import Listing
from reviews.models import Review
from bookings.models import Booking
from users.models import User
from locations.models import City, State, Country, Region  # ✅ Region добавлен

fake = Faker("de_DE")

# --- Настройки генерации ---
NUM_VISITORS = 25
NUM_LANDLORDS = 100
NUM_TENANTS = 50
NUM_LISTINGS = 200

PROPERTY_TYPES = ["apartment", "house", "studio", "loft", "villa"]

GERMAN_CITIES = [
    ("Berlin", "Berlin"),
    ("Munich", "Bavaria"),
    ("Hamburg", "Hamburg"),
    ("Cologne", "North Rhine-Westphalia"),
    ("Frankfurt", "Hesse"),
    ("Stuttgart", "Baden-Württemberg"),
    ("Dresden", "Saxony"),
    ("Leipzig", "Saxony"),
    ("Bremen", "Bremen"),
    ("Nuremberg", "Bavaria"),
]


# === Функции ===

def create_groups():
    for name in ["Tenant", "Landlord", "Visitor"]:
        Group.objects.get_or_create(name=name)
    print("✅ Groups created or verified")


def create_users():
    visitors, landlords, tenants = [], [], []

    for _ in range(NUM_VISITORS):
        username = f"{fake.user_name()}_visitor_{uuid.uuid4().hex[:6]}"
        visitors.append(User.objects.create_user(
            username=username,
            email=fake.email(),
            password="12345"
        ))

    for _ in range(NUM_LANDLORDS):
        username = f"{fake.user_name()}_landlord_{uuid.uuid4().hex[:6]}"
        user = User.objects.create_user(
            username=username,
            email=fake.email(),
            password="12345"
        )
        user.groups.add(Group.objects.get(name="Landlord"))
        landlords.append(user)

    for _ in range(NUM_TENANTS):
        username = f"{fake.user_name()}_tenant_{uuid.uuid4().hex[:6]}"
        user = User.objects.create_user(
            username=username,
            email=fake.email(),
            password="12345"
        )
        user.groups.add(Group.objects.get(name="Tenant"))
        tenants.append(user)

    print(f"✅ Users created: {len(visitors)} visitors, {len(landlords)} landlords, {len(tenants)} tenants")
    return landlords, tenants


def ensure_locations():
    """Создаёт регион, страну, штаты и города Германии"""
    region, _ = Region.objects.get_or_create(name="Europe")
    germany, _ = Country.objects.get_or_create(name="Germany", region=region)
    print("🌍 Country created or verified: Germany (Region: Europe)")

    states = {}
    cities = []

    for city_name, state_name in GERMAN_CITIES:
        if state_name not in states:
            state, _ = State.objects.get_or_create(name=state_name, country=germany)
            states[state_name] = state
        city, _ = City.objects.get_or_create(name=city_name, state=states[state_name])
        cities.append(city)

    print(f"🏙️  Verified {len(cities)} cities and {len(states)} states in Germany")
    return cities


def create_listings(landlords):
    listings = []
    cities = ensure_locations()

    for _ in range(NUM_LISTINGS):
        owner = random.choice(landlords)
        city = random.choice(cities)
        listing = Listing.objects.create(
            title=fake.sentence(nb_words=4),
            description=fake.paragraph(nb_sentences=3),
            owner=owner,
            price=round(random.uniform(50, 500), 2),
            price_currency="EUR",
            city=city,
            rooms=random.randint(1, 5),
            property_type=random.choice(PROPERTY_TYPES),
            is_available=True
        )
        listings.append(listing)

    print(f"🏠 Created {len(listings)} listings")
    return listings


def create_reviews(listings, tenants):
    for listing in random.sample(listings, k=int(len(listings) * 0.6)):
        for _ in range(random.randint(1, 3)):
            Review.objects.create(
                listing=listing,
                user=random.choice(tenants),
                rating=random.randint(3, 5),
                comment=fake.sentence()
            )
    print("💬 Reviews generated")


def create_bookings(listings, tenants):
    for _ in range(150):
        listing = random.choice(listings)
        tenant = random.choice(tenants)
        Booking.objects.create(
            listing=listing,
            tenant=tenant,
            status=random.choice(["approved", "pending", "completed"]),
            start_date=fake.date_this_year(before_today=True, after_today=False),
            end_date=fake.date_this_year(before_today=False, after_today=True)
        )
    print("📅 Bookings created")


# === Основной запуск ===
if __name__ == "__main__":
    print("🚀 Generating demo data...")
    create_groups()
    landlords, tenants = create_users()
    listings = create_listings(landlords)
    create_reviews(listings, tenants)
    create_bookings(listings, tenants)
    print("✅ Demo data generation completed successfully!")
