import os
from django.db import models
from shop.countries import COUNTRIES
from rest_framework.exceptions import ValidationError

from django.contrib import admin
import requests
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


def products_image_file_path(instance, filename):
    if instance.image_path:
        return os.path.join(instance.image_path, filename)
    else:
        return filename


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    manufacturer = models.CharField(
        max_length=255, blank=True, null=True, choices=COUNTRIES
    )
    image = models.ImageField(blank=True, null=True, upload_to=products_image_file_path)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    image_path = models.CharField(max_length=1024, blank=True, null=True)
    inventory = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title

    def clean(self):
        if self.inventory < 0:
            raise ValidationError({"inventory": "Inventory cannot be negative"})


class Cart(models.Model):
    user_id = models.UUIDField()
    items = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_id} - {self.items} - {self.quantity} - {self.created_at} - {self.updated_at}"


class MicroserviceUserProxy(models.Model):
    id = models.UUIDField(primary_key=True)
    email = models.EmailField()
    username = models.CharField(max_length=255)
    is_manager = models.BooleanField()
    is_moderator = models.BooleanField()

    class Meta:
        managed = False  # No database table creation or deletion operations will be performed for this model.
        verbose_name = 'User from Microservice'
        verbose_name_plural = 'Users from Microservice'

    def __str__(self):
        return self.email


"""Customised model for the administrator"""
class AdminManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class AdminUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    objects = AdminManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
