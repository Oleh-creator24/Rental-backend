from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Кастомная модель пользователя.
    Использует встроенную систему групп (Tenant, Landlord и Registered).
    """

    # Переопределяем ManyToMany поля, чтобы избежать конфликтов с related_name
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="user_groups",
        blank=True,
        verbose_name="группы",
        help_text="Группы, к которым принадлежит пользователь.",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="user_permissions_set",
        blank=True,
        verbose_name="права пользователя",
        help_text="Конкретные права пользователя.",
    )

    def __str__(self):
        group_names = ", ".join(self.groups.values_list("name", flat=True))
        return f"{self.username} ({group_names or 'No Group'})"

    # ---- Логика ролей ----
    @property
    def role(self) -> str:
        """
        Возвращает роль пользователя:
        Landlord | Tenant | Registered
        (Гость определяется по request.user.is_authenticated)
        """
        if self.groups.filter(name="Landlord").exists():
            return "Landlord"
        if self.groups.filter(name="Tenant").exists():
            return "Tenant"
        return "Registered"

    def is_tenant(self) -> bool:
        """Проверка — является ли пользователь арендатором"""
        return self.groups.filter(name="Tenant").exists()

    def is_landlord(self) -> bool:
        """Проверка — является ли пользователь арендодателем"""
        return self.groups.filter(name="Landlord").exists()
