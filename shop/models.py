from django.db import models
from shop.countries import COUNTRIES


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    manufacturer = models.CharField(max_length=255, blank=True, null=True, choices=COUNTRIES)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", default=1)

    class Meta:
        ordering = ["title"]
