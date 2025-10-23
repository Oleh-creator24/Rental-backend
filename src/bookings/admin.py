from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id", "tenant", "listing", "start_date", "end_date",
        "status", "is_deleted", "deleted_at", "created_at"
    )
    list_filter = ("status", "is_deleted", "created_at", "listing","start_date", "end_date")
    search_fields = ("tenant__username", "listing__title")
    ordering = ("-created_at",)
    actions = ["restore_bookings"]

    @admin.action(description="Восстановить выбранные бронирования")
    def restore_bookings(self, request, queryset):
        restored = queryset.update(is_deleted=False, deleted_at=None)
        self.message_user(request, f" Восстановлено {restored} бронирований.")
