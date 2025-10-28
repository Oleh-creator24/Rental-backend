from django.db import models
from django.conf import settings
from listings.models import Listing
from django.utils import timezone
from users.models import User



class ListingView(models.Model):
    """
    Модель фиксирует факт просмотра конкретного объявления.
    """
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="listing_views",
        null=True,  # разрешаем пустое значение
        blank=True  #  разрешаем не указывать при создании
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="listing_views_user",
        null=True,
        blank=True
    )
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"View {self.listing} by {self.user or 'Anonymous'}"


class SearchQuery(models.Model):
    """
    Модель хранит историю поисковых запросов пользователей.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="stats_queries",
    )
    query = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query '{self.query}' by {self.user}"

class SearchHistory(models.Model):
    """История поисковых запросов пользователей"""

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="search_history",
        verbose_name="Пользователь",
    )
    query = models.CharField(max_length=255, verbose_name="Поисковый запрос")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата поиска")
    count = models.PositiveIntegerField(default=1, verbose_name="Количество повторов")

    class Meta:
        verbose_name = "История поиска"
        verbose_name_plural = "История поисков"
        ordering = ["-created_at"]

    def __str__(self):
        user_str = self.user.username if self.user else "Аноним"
        return f"{user_str}: {self.query} ({self.count}×)"