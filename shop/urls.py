from django.urls import path, include
from rest_framework import routers
from shop.views import ProductViewSet, CategoryViewSet, CartViewSet, UserInfoView

router = routers.DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("products", ProductViewSet)
router.register("carts", CartViewSet)
from shop.views import UserInfoView



urlpatterns = [
    path("", include(router.urls)),
    path('user-info/', UserInfoView.as_view(), name='user-info'),
]

app_name = "product"
