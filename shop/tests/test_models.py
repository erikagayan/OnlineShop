from django.test import TestCase
from rest_framework.exceptions import ValidationError

from shop.models import Category, Product, Cart
from users.models import User


class CategoryModelTest(TestCase):
    def setUp(self):
        Category.objects.create(name="Electronics")
        Category.objects.create(name="Books")

    """Test category creation"""

    def test_category_creation(self):
        electronics = Category.objects.get(name="Electronics")
        books = Category.objects.get(name="Books")
        self.assertEqual(electronics.name, "Electronics")
        self.assertEqual(books.name, "Books")

    """Test category str"""

    def test_category_str(self):
        electronics = Category.objects.get(name="Electronics")
        self.assertEqual(str(electronics), "Electronics")

    "Test category ordering"

    def test_category_ordering(self):
        categories = list(Category.objects.all())
        self.assertLess(categories[0].name, categories[1].name)


class ProductModelTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Electronics")
        Product.objects.create(
            title="Laptop",
            price=1000,
            description="Powerful laptop",
            manufacturer="Manufacturer",
            category=category,
            inventory=10,
        )

    """Test product creation"""

    def test_product_creation(self):
        product = Product.objects.get(title="Laptop")
        self.assertEqual(product.title, "Laptop")
        self.assertEqual(product.price, 1000)
        self.assertEqual(product.description, "Powerful laptop")
        self.assertEqual(product.manufacturer, "Manufacturer")
        self.assertEqual(product.category.name, "Electronics")
        self.assertEqual(product.inventory, 10)

    """Test product str"""

    def test_product_str(self):
        product = Product.objects.get(title="Laptop")
        self.assertEqual(str(product), "Laptop")

    """Test product inventory validation"""

    def test_inventory_validation(self):
        product = Product.objects.get(title="Laptop")
        product.inventory = -5
        with self.assertRaises(ValidationError):
            product.clean()


class CartModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="ValidPassword123!"
        )
        category = Category.objects.create(name="Electronics")
        product = Product.objects.create(
            title="Laptop",
            price=1000,
            description="Powerful laptop",
            manufacturer="Manufacturer",
            category=category,
            inventory=10,
        )
        Cart.objects.create(user=user, items=product, quantity=2)

    """Test cart creation"""

    def test_cart_creation(self):
        cart = Cart.objects.first()
        self.assertEqual(cart.user.username, "testuser")
        self.assertEqual(cart.items.title, "Laptop")
        self.assertEqual(cart.quantity, 2)
