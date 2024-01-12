# Generated by Django 5.0 on 2024-01-12 09:53

import shop.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0008_alter_product_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to=shop.models.products_image_file_path
            ),
        ),
    ]