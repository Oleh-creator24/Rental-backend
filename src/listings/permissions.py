from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение: только владелец объекта может изменять или удалять.
    Остальные — только читать.
    """
    def has_object_permission(self, request, view, obj):
        # безопасные методы (GET, HEAD, OPTIONS) разрешены всем
        if request.method in permissions.SAFE_METHODS:
            return True
        # а изменения — только владельцу
        return obj.owner == request.user
