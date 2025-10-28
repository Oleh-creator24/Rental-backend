from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import Group
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор регистрации пользователя с выбором группы (Tenant / Landlord)
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)
    group = serializers.ChoiceField(
        choices=[("Tenant", "Tenant"), ("Landlord", "Landlord")],
        write_only=True  # 👈 добавили это
    )

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2", "group")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Пароли не совпадают."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        group_name = validated_data.pop("group")
        password = validated_data.pop("password")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=password,
        )

        try:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
        except Group.DoesNotExist:
            raise serializers.ValidationError({"group": f"Группа '{group_name}' не существует. Запусти init_groups."})

        return user



# === Новый сериализатор для входа по email ===
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Авторизация по username и password (по умолчанию).
    """
    def validate(self, attrs):
        print("DEBUG: attrs =", attrs)  # 🔍 покажет, что реально приходит
        username = attrs.get("username")
        password = attrs.get("password")
        print("DEBUG: username =", username, "password =", password)

        user = authenticate(username=username, password=password)
        print("DEBUG: authenticate() returned ->", user)

        if not user:
            raise serializers.ValidationError({"detail": "Неверное имя пользователя или пароль"})

        data = super().validate(attrs)
        print("DEBUG: data =", data)
        return data



