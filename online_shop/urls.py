from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/shop/", include("shop.urls", namespace="shop")),
    path("api/users/", include("users.urls", namespace="users")),
]
