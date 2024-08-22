import os
from django.db import models
from shop.countries import COUNTRIES
from rest_framework.exceptions import ValidationError


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
