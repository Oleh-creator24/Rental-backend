import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from listings.models import Listing
from reviews.models import Review

User = get_user_model()


@pytest.mark.django_db
class TestReviewsAPI:
    def setup_method(self):
        """Создаём пользователя, токен и тестовое объявление"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="reviewer",
            email="reviewer@example.com",
            password="StrongPass123"
        )

        # Авторизация
        token_url = reverse("token_obtain_pair")
        response = self.client.post(token_url, {
            "username": "reviewer",
            "password": "StrongPass123"
        })
        self.access_token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        # Создаём объявление
        self.listing = Listing.objects.create(
            title="Дом в Мюнхене",
            description="Уютный дом с садом",
            price=250.0,
            location="Munich",
            owner=self.user,
            is_available=True
        )

    def test_add_review(self):
        """Добавление отзыва к объявлению"""
        url = reverse("listing-reviews-list", args=[self.listing.id])
        data = {"rating": 5, "comment": "Отличный дом!"}
        response = self.client.post(url, data)
        assert response.status_code in [200, 201]
        assert Review.objects.filter(listing=self.listing, user=self.user).exists()

    def test_get_reviews(self):
        """Получение списка отзывов к объявлению"""
        # создаём один отзыв
        Review.objects.create(
            listing=self.listing,
            user=self.user,
            rating=4,
            comment="Неплохое жильё"
        )

        url = reverse("listing-reviews-list", args=[self.listing.id])
        response = self.client.get(url)
        assert response.status_code == 200

        # поддержка пагинации (results) или списка
        data = response.data.get("results", response.data)
        assert isinstance(data, list)
        assert len(data) >= 1
        assert "rating" in data[0]

    def test_allow_multiple_reviews_for_same_user(self):
        """Проверяем, что можно оставить несколько отзывов (если разрешено)"""
        url = reverse("listing-reviews-list", args=[self.listing.id])

        first = self.client.post(url, {"rating": 5, "comment": "Первый отзыв"})
        second = self.client.post(url, {"rating": 4, "comment": "Второй отзыв"})

        assert first.status_code in [200, 201]
        assert second.status_code in [200, 201]
        assert Review.objects.filter(listing=self.listing, user=self.user).count() >= 2
