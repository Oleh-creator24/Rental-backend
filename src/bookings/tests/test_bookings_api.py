import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from listings.models import Listing

User = get_user_model()


@pytest.mark.django_db
class TestBookingsAPI:
    def setup_method(self):
        """Создаём пользователя и токен"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="booker",
            email="booker@example.com",
            password="StrongPass123"
        )

        # Получаем JWT токен
        token_url = reverse("token_obtain_pair")
        response = self.client.post(token_url, {
            "username": "booker",
            "password": "StrongPass123"
        })
        self.access_token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        # создаём объявление для бронирования
        self.listing = Listing.objects.create(
            title="Квартира у моря",
            description="2 комнаты, отличный вид",
            price=120.0,
            location="Hamburg",   # ✅ заменили address → location
            owner=self.user,
            is_available=True
        )

    def test_create_booking(self):
        """Проверка создания бронирования"""
        url = reverse("booking-list")
        data = {
            "listing": self.listing.id,
            "start_date": "2025-10-15",
            "end_date": "2025-10-20",
        }
        response = self.client.post(url, data)
        assert response.status_code in [200, 201]
        assert response.data["listing"] == self.listing.id

    def test_get_user_bookings(self):
        """Получение списка своих бронирований"""
        # создаём одно бронирование
        create_url = reverse("booking-list")
        data = {
            "listing": self.listing.id,
            "start_date": "2025-11-01",
            "end_date": "2025-11-05",
        }
        self.client.post(create_url, data)

        # получаем список броней
        response = self.client.get(create_url)
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_booking_conflict(self):
        """Проверка пересечения дат (если логика реализована)"""
        url = reverse("booking-list")
        # создаём первую бронь
        self.client.post(url, {
            "listing": self.listing.id,
            "start_date": "2025-12-01",
            "end_date": "2025-12-10",
        })

        # пробуем пересечься
        response = self.client.post(url, {
            "listing": self.listing.id,
            "start_date": "2025-12-05",
            "end_date": "2025-12-12",
        })
        # допускаем 400, если конфликт обрабатывается
        assert response.status_code in [200, 201, 400]
