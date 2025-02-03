import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from shop.models import Category, Product, Cart
from shop.serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductListSerializer,
    CartSerializer,
)
from users.models import User


User = get_user_model()


# === FIXTURES ===


# === TESTS ===
@pytest.mark.category_serializer
def test_category_serializer(create_category):
    """Test category serializer."""
    category = create_category
    serializer = CategorySerializer(instance=category)
    data = serializer.data

    assert data["id"] == category.id
    assert data["name"] == category.name


@pytest.mark.product_serializer
def test_product_serializer(create_product):
    """Test product serializer."""
    product = create_product
    serializer = ProductSerializer(instance=product)
    data = serializer.data

    assert data["id"] == product.id
    assert data["title"] == product.title
    assert data["price"] == product.price
    assert data["description"] == product.description
    assert data["manufacturer"] == product.manufacturer
    assert data["category"] == product.category.id
    assert data["inventory"] == product.inventory


@pytest.mark.product_list_serializer
def test_product_list_serializer(create_product):
    """Test product list serializer."""
    product = create_product
    serializer = ProductListSerializer(instance=product)
    data = serializer.data

    assert data["id"] == product.id
    assert data["title"] == product.title
    assert data["price"] == product.price
    assert data["category"] == product.category.name
    assert data["inventory"] == product.inventory

    assert "description" not in data
    assert "manufacturer" not in data


@pytest.mark.cart_serializer
class TestCartSerializer:
    """Tests for CartSerializer."""

    def test_cart_serializer(self, create_cart_serializer):
        """
        Tests the correct serialisation of the shopping cart object.
        """
        serializer = create_cart_serializer["serializer"]
        cart = create_cart_serializer["cart"]
        data = serializer.data

        assert data["id"] == cart.id
        assert data["user"] == cart.user.id
        assert data["item_title"] == cart.items.title
        assert data["quantity"] == cart.quantity
        assert data["total_cost"] == cart.items.price * cart.quantity

    def test_cart_serializer_validation(self, create_cart_serializer):
        """
        Tests the validation of the data in the basket serialiser.
        If a quantity is passed that exceeds the available inventory, the validation should fail with an error with the ‘quantity’ key.
        """
        user = create_cart_serializer["user"]
        product = create_cart_serializer["product"]

        data = {
            "user": user.id,
            "items": product.id,
            "quantity": 20,
        }
        serializer = CartSerializer(data=data)
        assert not serializer.is_valid()
        assert "quantity" in serializer.errors
