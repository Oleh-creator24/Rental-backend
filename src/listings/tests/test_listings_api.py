import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestListingsAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="StrongPass123"
        )

        # Получаем токен для авторизации
        token_url = reverse("token_obtain_pair")
        response = self.client.post(token_url, {
            "username": "owner",
            "password": "StrongPass123"
        })
        self.access_token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_create_listing(self):
        """Создание объявления авторизованным пользователем"""
        url = reverse("listing-list")
        data = {
            "title": "Тестовое объявление",
            "description": "Простое описание",
            "price": 99.99,
            "address": "Berlin, Germany",
            "is_available": True,
        }
        response = self.client.post(url, data)
        assert response.status_code in [200, 201]
        assert response.data["title"] == "Тестовое объявление"

    def test_get_listings(self):
        """Получение списка объявлений"""
        url = reverse("listing-list")
        response = self.client.get(url)
        assert response.status_code == 200
        assert isinstance(response.data, list) or "results" in response.data

    def test_retrieve_listing(self):
        """Получение одного объявления"""
        # сначала создаём объявление
        create_url = reverse("listing-list")
        data = {
            "title": "Single listing",
            "description": "Desc",
            "price": 120,
            "address": "Munich",
            "is_available": True,
        }
        create_resp = self.client.post(create_url, data)
        listing_id = create_resp.data["id"]

        # теперь получаем его
        detail_url = reverse("listing-detail", args=[listing_id])
        response = self.client.get(detail_url)
        assert response.status_code == 200
        assert response.data["title"] == "Single listing"
