from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from users.models import User
from django.utils.translation import gettext as _


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {"fields": ("is_moderator", "is_manager", "is_staff", "groups")},
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "is_moderator", "is_manager")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)


"""
class UserAdmin(UserAdmin):
    list_display = ("username", "email", "is_moderator", "is_manager")
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (
            "Permissions",
            {"fields": ("is_moderator", "is_manager", "is_staff", "groups")},
        ),
    )
"""
