from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from shop.models import Category
from users.models import User


class CategoryViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="ValidPassword123!"
        )
        self.token = RefreshToken.for_user(self.user)
        self.admin_user = User.objects.create_superuser(
            username="adminuser",
            email="admin@example.com",
            password="AdminPassword123!",
        )

        self.category_data = {"name": "Electronics"}
        self.category = Category.objects.create(**self.category_data)

    def test_list_categories(self):
        url = reverse("product:category-list")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category_as_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}")
        url = reverse("product:category-list")
        response = self.client.post(url, self.category_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_category(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}")
        url = reverse("product:category-detail", args=[self.category.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_category_as_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}")
        url = reverse("product:category-detail", args=[self.category.pk])
        new_data = {"name": "Updated Category"}
        response = self.client.put(url, new_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_category_as_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}")
        url = reverse("product:category-detail", args=[self.category.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
