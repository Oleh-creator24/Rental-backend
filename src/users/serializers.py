from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import Group

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор регистрации пользователя с выбором группы (Tenant / Landlord)
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)
    group = serializers.ChoiceField(choices=[("Tenant", "Tenant"), ("Landlord", "Landlord")])

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2", "group")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Пароли не совпадают."})
        return attrs

    def create(self, validated_data):
        # Удаляем подтверждение пароля
        validated_data.pop("password2")

        # Извлекаем выбранную группу
        group_name = validated_data.pop("group")
        password = validated_data.pop("password")

        # Создаём пользователя
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=password,
        )

        # Добавляем в выбранную группу
        try:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
        except Group.DoesNotExist:
            raise serializers.ValidationError({"group": f"Группа '{group_name}' не существует. Запусти init_groups."})

        return user

class UserSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для отображения пользователя в других моделях (например, Booking)
    """
    class Meta:
        model = User
        fields = ["id", "username", "email"]
