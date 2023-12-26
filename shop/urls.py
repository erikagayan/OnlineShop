from django.urls import path, include
from rest_framework import routers
from shop.views import (
    ProductViewSet
)


router = routers.DefaultRouter()
router.register("products", ProductViewSet)


urlpatterns = [
    path("", include(router.urls)),
]

app_name = "product"
