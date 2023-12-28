from django.db import models
from shop.countries import COUNTRIES


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    manufacturer = models.CharField(max_length=255, blank=True, null=True, choices=COUNTRIES)
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    class Meta:
        ordering = ["title"]
