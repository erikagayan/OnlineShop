from django.test import TestCase
from shop.models import Category, Product, Cart
from shop.serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductListSerializer,
    CartSerializer,
)
from users.models import User


class CategorySerializerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.serializer = CategorySerializer(instance=self.category)

    """Test category serializer"""

    def test_category_serializer(self):
        data = self.serializer.data
        self.assertEqual(data["id"], self.category.id)
        self.assertEqual(data["name"], self.category.name)


class ProductSerializerTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            title="Laptop",
            price=1000,
            description="Powerful laptop",
            manufacturer="Manufacturer",
            category=category,
            inventory=10,
        )
        self.serializer = ProductSerializer(instance=self.product)

    """Test product serializer"""

    def test_product_serializer(self):
        data = self.serializer.data
        self.assertEqual(data["id"], self.product.id)
        self.assertEqual(data["title"], self.product.title)
        self.assertEqual(data["price"], self.product.price)
        self.assertEqual(data["description"], self.product.description)
        self.assertEqual(data["manufacturer"], self.product.manufacturer)
        self.assertEqual(data["category"], self.product.category.id)
        self.assertEqual(data["inventory"], self.product.inventory)


class ProductListSerializerTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            title="Laptop",
            price=1000,
            description="Powerful laptop",
            manufacturer="Manufacturer",
            category=category,
            inventory=10,
        )
        self.serializer = ProductListSerializer(instance=self.product)

    def test_product_list_serializer(self):
        data = self.serializer.data
        self.assertEqual(data["id"], self.product.id)
        self.assertEqual(data["title"], self.product.title)
        self.assertEqual(data["price"], self.product.price)
        self.assertEqual(data["category"], self.product.category.id)
        # Проверьте, что другие поля не находятся в сериализованных данных
        self.assertNotIn("description", data)
        self.assertNotIn("manufacturer", data)
        self.assertNotIn("inventory", data)


class CartSerializerTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="ValidPassword123!"
        )
        category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            title="Laptop",
            price=1000,
            description="Powerful laptop",
            manufacturer="Manufacturer",
            category=category,
            inventory=10,
        )
        self.cart = Cart.objects.create(user=user, items=self.product, quantity=2)
        self.serializer = CartSerializer(instance=self.cart)

    """Test cart serialization"""

    def test_cart_serializer(self):
        data = self.serializer.data
        self.assertEqual(data["id"], self.cart.id)
        self.assertEqual(data["user"], self.cart.user.id)
        self.assertEqual(data["item_title"], self.cart.items.title)
        self.assertEqual(data["quantity"], self.cart.quantity)
        self.assertEqual(data["total_cost"], self.cart.items.price * self.cart.quantity)

    """Test cart serializer validation"""

    def test_cart_serializer_validation(self):
        data = {
            "user": self.cart.user.id,
            "items": self.product.id,
            "quantity": 20,  # Exceeding available inventory
        }
        serializer = CartSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("quantity", serializer.errors)
