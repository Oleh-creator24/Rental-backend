from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Booking
from .serializers import BookingSerializer
from common.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated


@extend_schema_view(
    list=extend_schema(tags=["Bookings"]),
    retrieve=extend_schema(tags=["Bookings"]),
    create=extend_schema(tags=["Bookings"]),
    update=extend_schema(tags=["Bookings"]),
    partial_update=extend_schema(tags=["Bookings"]),
    destroy=extend_schema(tags=["Bookings"]),
    approve=extend_schema(tags=["Bookings"], summary="Подтвердить бронирование"),
    reject=extend_schema(tags=["Bookings"], summary="Отклонить бронирование"),
    cancel=extend_schema(tags=["Bookings"], summary="Отменить бронирование"),
)
class BookingViewSet(viewsets.ModelViewSet):
    """CRUD операции и управление бронированиями"""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        """Не показывать удалённые бронирования в API"""
        return Booking.objects.filter(is_deleted=False).order_by("-created_at")

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        """Подтверждение бронирования арендодателем"""
        booking = self.get_object()
        booking.status = "approved"
        booking.save()
        return Response({"status": "approved"})

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        """Отклонение бронирования"""
        booking = self.get_object()
        booking.status = "rejected"
        booking.save()
        return Response({"status": "rejected"})

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        """Отмена бронирования пользователем"""
        booking = self.get_object()
        booking.status = "canceled"
        booking.save()
        return Response({"status": "canceled"})
