from django.contrib import admin
from .models import ListingView, SearchQuery,SearchHistory

@admin.register(ListingView)
class ListingViewAdmin(admin.ModelAdmin):
    list_display = ("listing", "user", "viewed_at")
    list_filter = ("viewed_at",)
    search_fields = ("listing__title", "user__username")

@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ("query", "user", "created_at")
    search_fields = ("query", "user__username")
    ordering = ("-created_at",)

@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ("query", "user", "count", "created_at")
    list_filter = ("user",)
    search_fields = ("query", "user__username")
    ordering = ("-count", "-created_at")