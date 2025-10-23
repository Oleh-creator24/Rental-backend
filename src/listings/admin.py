from django.contrib import admin
from .models import Listing, ListingView

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        "id", "title", "owner", "price", "price_currency",
        "is_available", "view_count", "created_at"
    )
    list_filter = ("is_available", "price_currency", "city", "country")
    search_fields = ("title", "description", "street", "city__name", "country")
    ordering = ("-created_at",)
    readonly_fields = ("view_count",)
    date_hierarchy = "created_at"

@admin.register(ListingView)
class ListingViewAdmin(admin.ModelAdmin):
    list_display = ("listing", "user", "ip_address", "viewed_at")
    list_filter = ("viewed_at", "listing")
    search_fields = ("listing__title", "user__username", "ip_address")
    ordering = ("-viewed_at",)
