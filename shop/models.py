from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.IntegerField(default=0)

    class Meta:
        ordering = ["title"]
