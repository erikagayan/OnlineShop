import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from shop.models import Category, Product, Cart


User = get_user_model()

# === FIXTURES ===
@pytest.fixture
def create_user(db):
    """Fixture to create a test user."""
    return User.objects.create_user(
        username="testuser", email="test@example.com", password="ValidPassword123!"
    )


@pytest.fixture
def create_cart(db, create_user, create_categories):
    """Fixture to create a test cart."""
    category = Category.objects.get(
        name="Electronics"
    )
    product = Product.objects.create(
        title="Laptop",
        price=1000,
        description="Powerful laptop",
        manufacturer="Manufacturer",
        category=category,
        inventory=10,
    )
    return Cart.objects.create(user=create_user, items=product, quantity=2)


# === TESTS ===


# --- CATEGORY TESTS ---
@pytest.mark.category
class TestCategory:
    """Test suite for Category model."""

    def test_category_creation(self, create_categories):
        """Test category creation."""
        electronics = Category.objects.get(name="Electronics")
        books = Category.objects.get(name="Books")
        assert electronics.name == "Electronics"
        assert books.name == "Books"

    def test_category_str(self, create_categories):
        """Test category __str__ method."""
        electronics = Category.objects.get(name="Electronics")
        assert str(electronics) == "Electronics"

    def test_category_ordering(self, create_categories):
        """Test category ordering."""
        categories = list(Category.objects.all())
        assert categories[0].name < categories[1].name


# --- PRODUCT TESTS ---
@pytest.mark.product
class TestProduct:
    """Test suite for Product model."""

    def test_product_creation(self, create_product):
        """Test product creation."""
        product = Product.objects.get(title="Laptop")
        assert product.title == "Laptop"
        assert product.price == 1000
        assert product.description == "Powerful laptop"
        assert product.manufacturer == "Manufacturer"
        assert product.category.name == "Electronics"
        assert product.inventory == 10

    def test_product_str(self, create_product):
        """Test product __str__ method."""
        product = Product.objects.get(title="Laptop")
        assert str(product) == "Laptop"

    def test_inventory_validation(self, create_product):
        """Test product inventory validation."""
        product = Product.objects.get(title="Laptop")
        product.inventory = -5
        with pytest.raises(ValidationError):
            product.clean()


# --- CART TESTS ---
@pytest.mark.cart
class TestCart:
    """Test suite for Cart model."""

    def test_cart_creation(self, create_cart):
        """Test cart creation."""
        cart = Cart.objects.first()
        assert cart.user.username == "testuser"
        assert cart.items.title == "Laptop"
        assert cart.quantity == 2
