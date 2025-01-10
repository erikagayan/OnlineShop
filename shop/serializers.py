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
        fields = ["id", "title", "price", "category", "inventory"]


class CartSerializer(serializers.ModelSerializer):
    item_title = serializers.CharField(source="items.title", read_only=True)
    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "user",
            "item_title",
            "items",
            "quantity",
            "created_at",
            "updated_at",
            "total_cost",
        ]
        read_only_fields = ["user", "item_title", "total_cost"]
        extra_kwargs = {"items": {"write_only": True}}  # Making items writable only

    def get_total_cost(self, obj):
        """Calculating the total amount"""
        total = 0
        for item in Cart.objects.filter(user=obj.user):
            total += item.items.price * item.quantity
        return total

    def get_item_title(self, obj):
        return obj.items.title if obj.items else None

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
