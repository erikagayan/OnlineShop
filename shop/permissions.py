from rest_framework import permissions


class IsManagerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow managers to edit products, and allow anyone to view products.
    """
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.is_manager

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or request.user.is_manager
