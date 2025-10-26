from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("listing__title", "user__username", "comment")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
