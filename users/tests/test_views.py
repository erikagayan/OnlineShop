import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="ValidPassword123!"
        )
        self.token = RefreshToken.for_user(self.user)

    def test_create_token(self):
        url = reverse("users:token")
        data = {"email": "test@example.com", "password": "ValidPassword123!"}
        response = self.client.post(url, data)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response_data)
        self.assertIn("refresh", response_data)

    def test_retrieve_user(self):
        url = reverse("users:manage")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "test@example.com")

    def test_update_user_password(self):
        url = reverse("users:manage")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}")
        updated_data = {
            "username": self.user.username,
            "email": self.user.email,
            "password": "NewValidPassword123!",
        }
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(updated_data["password"]))
