import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestAuthAPI:

    def setup_method(self):
        """Создаём клиент перед каждым тестом"""
        self.client = APIClient()

    def test_user_registration(self):
        """Проверка регистрации нового пользователя"""
        url = reverse("register")
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "StrongPass123",
            "password2": "StrongPass123",
        }
        response = self.client.post(url, data)
        print("Response data:", response.data)  # удобно для отладки
        assert response.status_code in [200, 201]
        assert User.objects.filter(username="newuser").exists()

    def test_jwt_token_obtain(self):
        """Проверка получения JWT токена"""
        user = User.objects.create_user(username="tester", password="12345")
        url = reverse("token_obtain_pair")  # из config/urls.py
        data = {"username": "tester", "password": "12345"}
        response = self.client.post(url, data)
        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    def test_jwt_token_refresh(self):
        """Проверка обновления токена"""
        user = User.objects.create_user(username="refresher", password="12345")
        login_url = reverse("token_obtain_pair")
        refresh_url = reverse("token_refresh")

        # Получаем токен
        login_response = self.client.post(login_url, {"username": "refresher", "password": "12345"})
        assert login_response.status_code == 200
        refresh_token = login_response.data["refresh"]

        # Обновляем токен
        response = self.client.post(refresh_url, {"refresh": refresh_token})
        assert response.status_code == 200
        assert "access" in response.data
