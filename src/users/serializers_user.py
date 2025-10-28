from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для отображения пользователя в других моделях (например, Booking)
    """
    class Meta:
        model = User
        fields = ["id", "username", "email"]
