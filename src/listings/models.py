from django.db import models
from users.models import User
from locations.models import City
from django.core.validators import MinValueValidator
from django.utils import timezone

CURRENCY_CHOICES = [
    ("EUR", "Euro"),
    ("USD", "US Dollar"),
    ("GBP", "Pound Sterling"),
    ("CHF", "Swiss Franc"),
    ("PLN", "Polish Zloty"),
    ("CZK", "Czech Koruna"),
]

PROPERTY_TYPE_CHOICES = [
    ("house", "Дом"),
    ("apartment", "Квартира"),
    ("studio", "Студия"),
    ("room", "Комната"),
]


class Listing(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="listings",
        verbose_name="Владелец",
    )
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")

    # 🔹 Цена и валюта
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1)],
        verbose_name="Цена",
    )
    price_currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default="EUR",
        verbose_name="Валюта",
    )

    # 🔹 Тип жилья и комнаты
    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPE_CHOICES,
        default="apartment",
        verbose_name="Тип жилья",
    )
    rooms = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name="Количество комнат",
    )

    # 🔹 Средний рейтинг и доступность
    rating = models.FloatField(default=0, verbose_name="Рейтинг")
    is_available = models.BooleanField(default=True, verbose_name="Активно")

    # 🔹 Адрес
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="listings",
        verbose_name="Город",
    )
    street = models.CharField(max_length=255, verbose_name="Улица")
    house_number = models.CharField(max_length=10, verbose_name="Номер дома")
    apartment_number = models.CharField(
        max_length=10, null=True, blank=True, verbose_name="Квартира"
    )

    # 🔹 Статистика
    view_count = models.PositiveIntegerField(default=0, verbose_name="Просмотры")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "title", "street", "house_number", "apartment_number"],
                name="unique_owner_listing_address",
            )
        ]

    def __str__(self):
        """Строковое представление объекта"""
        city_name = self.city.name if self.city else "Неизвестный город"
        if self.apartment_number:
            return f"{self.title} — {city_name}, {self.street} {self.house_number}, кв. {self.apartment_number}"
        return f"{self.title} — {city_name}, {self.street} {self.house_number}"


class ListingView(models.Model):
    """История просмотров объявлений пользователями"""

    listing = models.ForeignKey(
        "Listing",
        on_delete=models.CASCADE,
        related_name="views",
        verbose_name="Объявление",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="listing_views",
        verbose_name="Пользователь",
    )
    ip_address = models.GenericIPAddressField(
        null=True, blank=True, verbose_name="IP-адрес"
    )
    viewed_at = models.DateTimeField(default=timezone.now, verbose_name="Дата просмотра")

    class Meta:
        verbose_name = "Просмотр объявления"
        verbose_name_plural = "История просмотров"
        ordering = ["-viewed_at"]

    def __str__(self):
        user_str = self.user.username if self.user else "Аноним"
        return f"{user_str} → {self.listing.title} ({self.viewed_at.strftime('%Y-%m-%d %H:%M')})"
