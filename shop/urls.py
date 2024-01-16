from django.urls import path, include
from rest_framework import routers
from shop.views import ProductViewSet, CategoryViewSet, CartViewSet


router = routers.DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("products", ProductViewSet)
router.register("carts", CartViewSet)


urlpatterns = [
    path("", include(router.urls)),
]

app_name = "product"
