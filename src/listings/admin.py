from django.contrib import admin
from .models import Listing, ListingView


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "city",
        "price",
        "rooms",
        "property_type",
        "is_available",
        "owner",
        "created_at",
    )
    list_filter = (
        "city",
        "property_type",
        "is_available",
        "created_at",
    )
    search_fields = (
        "title",
        "description",
        "owner__email",
        "city__name",
    )
    list_per_page = 20
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)


@admin.register(ListingView)
class ListingViewAdmin(admin.ModelAdmin):
    list_display = ("listing", "user", "ip_address", "viewed_at")
    list_filter = ("viewed_at", "listing")
    search_fields = ("listing__title", "user__username", "ip_address")
    ordering = ("-viewed_at",)
