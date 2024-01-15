from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from shop.permissions import IsStaffOrReadOnly
from shop.serializers import (
    ProductSerializer,
    ProductListSerializer,
    CategorySerializer,
)
from shop.models import Product, Category


class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]


class ProductViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        return ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        order_by = self.request.query_params.get("order_by", None)
        if order_by == "price":
            queryset = queryset.order_by("price")
        elif order_by == "category":
            queryset = queryset.order_by("category")
        return queryset

    """Inventory cannot be negative during create"""
    def perform_create(self, serializer):
        inventory = int(self.request.data.get("inventory", 0))
        if inventory < 0:
            return Response(
                {"inventory": "Inventory cannot be negative."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()

    """Inventory cannot be negative during update"""
    def perform_update(self, serializer):
        inventory = int(self.request.data.get("inventory", 0))
        if inventory < 0:
            return Response(
                {"inventory": "Inventory cannot be negative."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()
