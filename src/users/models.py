from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_set",
        blank=True,
    )

    def __str__(self):
        group_names = ", ".join(self.groups.values_list("name", flat=True))
        return f"{self.username} ({group_names or 'No Group'})"
