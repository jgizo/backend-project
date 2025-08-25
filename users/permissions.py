from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "admin"

class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return getattr(obj, "owner", None) == request.user or request.user.role == "admin"
    
class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "mod"
    