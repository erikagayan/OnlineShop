from rest_framework import permissions


def is_manager_or_moderator_or_superuser(user):
    return user.is_manager or user.is_moderator or user.is_superuser

class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow managers to edit products, and allow anyone to view products.
    """
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or is_manager_or_moderator_or_superuser(request.user)

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or is_manager_or_moderator_or_superuser(request.user)
