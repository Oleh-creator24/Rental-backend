from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User



@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Кастомная админка пользователей с отображением ролей и групп.
    """

    list_display = ("username", "email", "role", "is_active", "is_staff", "date_joined")
    list_filter = ("is_active", "is_staff", "groups")
    search_fields = ("username", "email")
    ordering = ("-date_joined",)
    readonly_fields = ("last_login", "date_joined")

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "groups"),
        }),
    )

    def role(self, obj):
        return obj.role

    role.short_description = "Роль"


#  Регистрируем в стандартной админке
# (чтобы избежать цикла, подключим custom_admin_site позже)
try:
    from src.config.admin_dashboard import custom_admin_site
    custom_admin_site.register(User, UserAdmin)
except Exception:
    # Во время миграций admin_dashboard может быть ещё не загружен — пропускаем
    pass
