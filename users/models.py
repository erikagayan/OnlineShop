from django.db import models
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    """Model manager for creating users without using the username field"""

    # specifies that this manager should be used for migrations
    use_in_migrations = True

    def _create_user(self, email, username, password, **extra_fields):
        """Private method, Create and save a User with the given email, username and password."""

        if not email:
            raise ValueError("The given email must be set")
        if not username:
            raise ValueError("The given username must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        """Create and save a regular User with the given email, username and password."""

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        # Calls the _create_user private method to create and save a user.
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password, **extra_fields):
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
        if self.email and not self.email.endswith('@example.com'):
            raise ValidationError(_('Email address must be from the example.com domain'))

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
