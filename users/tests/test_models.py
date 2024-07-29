from users.models import User
from django.test import TestCase


class UserTestCase(TestCase):
    """Unittest for User model"""
    def setUp(self):
        self.email = "test@example.com"
        self.username = "testuser"
        self.password = "testpassword123"

    """Create user"""

    def test_create_user(self):
        user = User.objects.create_user(
            email=self.email, username=self.username, password=self.password
        )
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.username, self.username)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password(self.password))

    """Create superuser"""

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            email=self.email, username=self.username, password=self.password
        )
        self.assertEqual(superuser.email, self.email)
        self.assertEqual(superuser.username, self.username)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.check_password(self.password))

    """Create user without email"""

    def test_user_without_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="", username=self.username, password=self.password
            )

    """Create user without username"""

    def test_user_without_username(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email=self.email, username="", password=self.password
            )
