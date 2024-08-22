import requests
from rest_framework import serializers
from shop.models import Product, Category, Cart


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

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
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ["id", "title", "price", "category"]


class CartSerializer(serializers.ModelSerializer):
    item_title = serializers.CharField(source="items.title", read_only=True)
    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "user_id",
            "item_title",
            "items",
            "quantity",
            "created_at",
            "updated_at",
            "total_cost",
        ]
        read_only_fields = ["item_title", "total_cost"]
        extra_kwargs = {"items": {"write_only": True}}

    def get_total_cost(self, obj):
        total = 0
        for item in Cart.objects.filter(user_id=obj.user_id):
            total += item.items.price * item.quantity
        return total

    def validate(self, data):
        if data["quantity"] > data["items"].inventory:
            available_stock = data["items"].inventory
            raise serializers.ValidationError(
                {"quantity": f"Not enough stock. {available_stock} left"}
            )
        return data
