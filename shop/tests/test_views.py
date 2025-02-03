import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from shop.models import Category
from users.models import User


@pytest.mark.category_view
class TestCategoryViewSet:
    """Тесты для CategoryViewSet с использованием фикстур setup_views и api_client."""

    def test_list_categories(self, setup_views, api_client):
        """
        Тест получения списка категорий:
        - Авторизация через JWT обычного пользователя.
        - Ожидается статус 200 OK.
        """
        token = setup_views["token"]
        url = reverse("product:category-list")
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_create_category_as_user(self, setup_views, api_client):
        """
        Тест попытки создания категории обычным пользователем:
        - Авторизация через JWT обычного пользователя.
        - Ожидается, что операция запрещена (403 Forbidden).
        """
        token = setup_views["token"]
        url = reverse("product:category-list")
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
        response = api_client.post(url, setup_views["category_data"])
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_category(self, setup_views, api_client):
        """
        Тест получения деталей категории:
        - Авторизация через JWT обычного пользователя.
        - Ожидается статус 200 OK.
        """
        token = setup_views["token"]
        category = setup_views["category"]
        url = reverse("product:category-detail", args=[category.pk])
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_update_category_as_user(self, setup_views, api_client):
        """
        Тест попытки обновления категории обычным пользователем:
        - Авторизация через JWT обычного пользователя.
        - Ожидается, что операция запрещена (403 Forbidden).
        """
        token = setup_views["token"]
        category = setup_views["category"]
        url = reverse("product:category-detail", args=[category.pk])
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
        new_data = {"name": "Updated Category"}
        response = api_client.put(url, new_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_category_as_user(self, setup_views, api_client):
        """
        Тест попытки удаления категории обычным пользователем:
        - Авторизация через JWT обычного пользователя.
        - Ожидается, что операция запрещена (403 Forbidden).
        """
        token = setup_views["token"]
        category = setup_views["category"]
        url = reverse("product:category-detail", args=[category.pk])
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
