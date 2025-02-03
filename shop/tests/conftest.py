import pytest
from rest_framework.test import APIClient
from shop.serializers import CartSerializer
from django.contrib.auth import get_user_model
from shop.models import Category, Product, Cart
from rest_framework_simplejwt.tokens import RefreshToken

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


@pytest.fixture
def setup_views(db):
    user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="ValidPassword123!"
    )
    token = RefreshToken.for_user(user)
    admin_user = User.objects.create_superuser(
        username="adminuser",
        email="admin@example.com",
        password="AdminPassword123!"
    )
    category_data = {"name": "Electronics"}
    category = Category.objects.create(**category_data)

    return {
        "user": user,
        "token": token,
        "admin_user": admin_user,
        "category_data": category_data,
        "category": category,
    }


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture(autouse=True)
def disable_cache(settings):
    settings.CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
