import pytest
from shop.serializers import CartSerializer
from django.contrib.auth import get_user_model
from shop.models import Category, Product, Cart

User = get_user_model()

@pytest.fixture
def create_category(db):
    """Fixture to create a test category."""
    return Category.objects.create(name="Electronics")

@pytest.fixture
def create_categories(db):
    """Fixture to create test categories."""
    Category.objects.create(name="Electronics")
    Category.objects.create(name="Books")

@pytest.fixture
def create_product(db, create_categories):
    """Fixture to create a test product."""
    category = Category.objects.get(name="Electronics")
    return Product.objects.create(
        title="Laptop",
        price=1000,
        description="Powerful laptop",
        manufacturer="Manufacturer",
        category=category,
        inventory=10,
    )

@pytest.fixture
def create_cart_serializer(db):
    """
    Fixture for creating user, category, product, basket and serialiser.
    """
    user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="ValidPassword123!"
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
    cart = Cart.objects.create(user=user, items=product, quantity=2)
    serializer = CartSerializer(instance=cart)
    return {
        "user": user,
        "category": category,
        "product": product,
        "cart": cart,
        "serializer": serializer,
    }

