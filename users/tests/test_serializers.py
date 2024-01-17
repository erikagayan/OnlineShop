from django.test import TestCase
from rest_framework.exceptions import ValidationError
from users.serializers import UserSerializer
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class UserSerializerTestCase(TestCase):
    def setUp(self):
        User.objects.all().delete()
        self.user_data = {
            "username": f"testuser{uuid.uuid4()}",
            "email": f"test{uuid.uuid4()}@example.com",
            "password": "ValidPassword123!",
        }
        self.user = User.objects.create_user(**self.user_data)

    """Test serialization"""

    def test_serialization(self):
        serializer = UserSerializer(instance=self.user)
        data = serializer.data
        self.assertEqual(data["username"], self.user.username)
        self.assertEqual(data["email"], self.user.email)
        self.assertNotIn("password", data)

    """Test validate password"""

    def test_validate_password(self):
        invalid_password_data = self.user_data.copy()
        invalid_password_data["password"] = "11111"

        with self.assertRaises(ValidationError):
            serializer = UserSerializer(data=invalid_password_data)
            serializer.is_valid(raise_exception=True)

    """Test update password"""

    def test_update_user_password(self):
        update_data = {"password": "NewValidPassword123!"}
        serializer = UserSerializer(instance=self.user, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertTrue(user.check_password(update_data["password"]))


class UserSerializerCreateTest(TestCase):
    def setUp(self):
        unique_id = uuid.uuid4()
        self.user_data = {
            "username": f"testuser{unique_id}",
            "email": f"test{unique_id}@example.com",
            "password": "ValidPassword123!",
        }

    """Test create user"""

    def test_create_user(self):
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.username, self.user_data["username"])
        self.assertEqual(user.email, self.user_data["email"])
        self.assertTrue(user.check_password(self.user_data["password"]))
