from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, username, password, **extra_fields):
        """Create and save a User with the given email, username and password."""
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
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password, **extra_fields):
        """Create and save a SuperUser with the given email, username and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        # ... проверки на is_staff и is_superuser ...
        return self._create_user(email, username, password, **extra_fields)


class User(AbstractUser):
    is_moderator = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(_("username"), unique=True, max_length=150)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()
