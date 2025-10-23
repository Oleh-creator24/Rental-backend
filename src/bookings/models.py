from django.db import models
from django.conf import settings
from listings.models import Listing
from django.utils import timezone


class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Ожидает подтверждения"),
        ("approved", "Подтверждено"),
        ("rejected", "Отклонено"),
        ("canceled", "Отменено"),
    ]

    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="Арендатор",
        null=True,
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="Объявление",
    )
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="Статус",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    # --- Мягкое удаление ---
    is_deleted = models.BooleanField(default=False, verbose_name="Удалено")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата удаления")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

    def __str__(self):
        return f"{self.listing.title} ({self.start_date} — {self.end_date})"

    def clean(self):
        """Проверка: дата окончания не раньше даты начала."""
        if self.end_date < self.start_date:
            raise ValueError("Дата окончания не может быть раньше даты начала")

    def save(self, *args, **kwargs):
        """Валидация перед сохранением."""
        self.clean()
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        """Мягкое удаление: отметка как удалённой без физического удаления."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        """Восстановление мягко удалённой брони."""
        self.is_deleted = False
        self.deleted_at = None
        self.save()
