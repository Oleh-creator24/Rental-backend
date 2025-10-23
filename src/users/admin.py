from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

User = get_user_model()


# 👇 Кастомный фильтр по группам
class GroupFilter(admin.SimpleListFilter):
    title = "By group"
    parameter_name = "group"

    def lookups(self, request, model_admin):
        """Доступные варианты фильтра"""
        return [
            ("tenant", "Tenant"),
            ("landlord", "Landlord"),
            ("none", "No Group"),
        ]

    def queryset(self, request, queryset):
        """Фильтрация пользователей по группам"""
        if self.value() == "tenant":
            return queryset.filter(groups__name="Tenant")
        elif self.value() == "landlord":
            return queryset.filter(groups__name="Landlord")
        elif self.value() == "none":
            return queryset.filter(groups__isnull=True)
        return queryset


#  Единый класс админки для User
@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """
    Кастомная админка пользователя с фильтром по группам
    и отображением ролей (Tenant / Landlord / и т.д.).
    """

    list_display = ("username", "email", "display_groups", "is_staff", "is_active", "is_superuser")
    list_filter = ("is_staff", "is_superuser", "is_active", GroupFilter)
    search_fields = ("username", "email")
    ordering = ("username",)
    filter_horizontal = ("groups", "user_permissions")

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username", "email", "password1", "password2",
                "is_staff", "is_active", "is_superuser", "groups"
            ),
        }),
    )

    def display_groups(self, obj):
        """Отображает список групп (Tenant / Landlord / и т.д.)"""
        groups = obj.groups.values_list("name", flat=True)
        return ", ".join(groups) if groups else "—"

    display_groups.short_description = "Groups"


#  Регистрируем модель Group отдельно (если не отображается)
try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass

admin.site.register(Group)
