from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsLandlord(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, "role", None) == "landlord"

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and getattr(obj, "owner_id", None) == request.user.id
