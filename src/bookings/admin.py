from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "tenant", "status", "start_date", "end_date", "created_at")
    list_filter = ("status", "created_at", "updated_at")
    search_fields = ("listing__title", "tenant__username")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
