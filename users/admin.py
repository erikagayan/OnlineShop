from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


class UserAdmin(UserAdmin):
    list_display = ("username", "email", "is_moderator", "is_manager")
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Permissions", {"fields": ("is_moderator", "is_manager")}),
    )

admin.site.register(User, UserAdmin)
