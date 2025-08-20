from django.db import models
from typing import Any, Optional
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    """Model manager for creating users without using the username field"""

    # specifies that this manager should be used for migrations
    use_in_migrations = True

    def _create_user(
        self, email: str, username: str, password: str, **extra_fields: Any
    ) -> Any:
        """
        Private method, Create and save a User with the given email, username and password in DB.
        Raises: ValueError: If email, username, or password is not provided.
        """

        missing_fields = [
            field
            for field, value in {
                "email": email,
                "username": username,
                "password": password,
            }.items()
            if not value
        ]

        if missing_fields:
            raise ValueError(
                f"The following fields must be set: {', '.join(missing_fields)}"
            )

        email = self.normalize_email(email)
        # create user
        user = self.model(email=email, username=username, **extra_fields)
        # create password
        user.set_password(password)
        # save user
        user.save(using=self._db)
        return user

    def create_user(
        self,
        email: str,
        username: str,
        password: Optional[str] = None,
        **extra_fields: Any,
    ) -> Any:
        """Create and save a regular User with the given email, username and password."""

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        # Calls the _create_user private method to create and save a user.
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(
        self, email: str, username: str, password: str, **extra_fields: Any
    ) -> Any:
        """Create and save a SuperUser with the given email, username and password."""

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Calls the _create_user private method to create and save a superuser.
        return self._create_user(email, username, password, **extra_fields)


class User(AbstractUser):
    """User model"""

    is_moderator = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(_("username"), unique=True, max_length=150)
    telegram_chat_id = models.CharField(
        max_length=50, null=True, blank=True, unique=True
    )

    # Email for auth
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    # For this model you should use the custom UserManager
    objects = UserManager()

    def __str__(self):
        return self.email

    def clean(self):
        super().clean()

        # addition email validation
        if self.email and not self.email.endswith("@example.com"):
            raise ValidationError(
                _("Email address must be from the example.com domain")
            )

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


class TelegramToken(models.Model):
    """Model for temporary tokens for Telegram connection"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="telegram_tokens"
    )
    token = models.CharField(max_length=36, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token {self.token} for {self.user.email}"
