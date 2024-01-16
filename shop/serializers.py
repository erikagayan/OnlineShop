from rest_framework import serializers
from shop.models import Product, Category, Cart


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "price",
            "description",
            "manufacturer",
            "category",
            "inventory",
        ]


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "price", "category"]


class CartSerializer(serializers.ModelSerializer):
    items = serializers.CharField(source="items.title", read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "items", "quantity", "created_at", "updated_at"]
        read_only_fields = ["user"]

    def validate(self, data):
        """
        Checking if there are enough goods in stock.
        """
        if data["quantity"] > data["items"].inventory:
            available_stock = data["items"].inventory
            raise serializers.ValidationError(
                {"quantity": f"Not enough stock. {available_stock} left"}
            )
        return data
