# Generated by Django 5.0 on 2023-12-28 14:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0003_alter_product_manufacturer"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="products/"),
        ),
    ]