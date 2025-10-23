from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import UserRegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

User = get_user_model()


@extend_schema_view(
    create=extend_schema(tags=["Users"], summary="Регистрация нового пользователя")
)
class RegisterView(generics.CreateAPIView):
    """Регистрация нового пользователя"""
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


@extend_schema(
    tags=["Users"],
    summary="Получение данных текущего пользователя"
)
class MeView(APIView):
    """Информация о текущем авторизованном пользователе"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": getattr(user, "role", None),
        })
