from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema
from .serializers import CustomTokenObtainPairSerializer


@extend_schema(
    tags=["Auth"],
    summary="Авторизация пользователя (логин)",
    description="Получение пары токенов (access и refresh) по email и паролю."
)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema(
    tags=["Auth"],
    summary="Обновление access токена",
    description="Обновление токена доступа по refresh токену."
)
class CustomTokenRefreshView(TokenRefreshView):
    pass
