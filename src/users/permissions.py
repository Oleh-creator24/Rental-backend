from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedOrReadOnly(BasePermission):
    """
    Разрешает просмотр всем пользователям, но модификацию — только авторизованным.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


class IsTenant(BasePermission):
    """
    Разрешает доступ только пользователям из группы Tenant (арендатор).
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name="Tenant").exists()
        )


class IsLandlord(BasePermission):
    """
    Разрешает доступ только пользователям из группы Landlord (арендодатель).
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name="Landlord").exists()
        )


class IsOwnerOrAdmin(BasePermission):
    """
    Разрешает действия только владельцу объекта (owner/tenant/user) или администратору.
    Используется в объектах Booking, Listing, Review.
    """
    def has_object_permission(self, request, view, obj):
        # суперпользователь и staff всегда имеют доступ
        if request.user.is_staff or request.user.is_superuser:
            return True

        # если есть поле owner, tenant или user — сравниваем с текущим пользователем
        owner = getattr(obj, "owner", None) or getattr(obj, "tenant", None) or getattr(obj, "user", None)
        return owner == request.user


class ReadOnly(BasePermission):
    """
    Полностью запрещает изменение — разрешает только чтение (GET, HEAD, OPTIONS).
    """
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsAdmin(BasePermission):
    """
    Доступ только для администраторов (staff или superuser).
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or request.user.is_superuser
        )
