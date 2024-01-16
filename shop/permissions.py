from rest_framework import permissions


def is_manager_or_moderator_or_superuser(user):
    return user.is_manager or user.is_moderator or user.is_superuser


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow managers to edit products, and allow anyone to view products.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or is_manager_or_moderator_or_superuser(request.user)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or is_manager_or_moderator_or_superuser(request.user)
        )


class IsOwnerOrStaff(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Assumes the model instance has an `user` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the cart or staff.
        return obj.user == request.user or is_manager_or_moderator_or_superuser(request.user)
