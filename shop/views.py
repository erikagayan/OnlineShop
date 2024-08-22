from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from shop.models import Product, Category, Cart
from rest_framework import viewsets, mixins, status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from shop.authentication import MicroserviceJWTAuthentication
from shop.permissions import IsStaffOrReadOnly, IsOwnerOrStaff
from shop.serializers import (
    ProductSerializer,
    ProductListSerializer,
    CategorySerializer,
    CartSerializer,
)


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
    authentication_classes = [MicroserviceJWTAuthentication]
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]

    @method_decorator(cache_page(10))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


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

        """Only for documentation"""
        @extend_schema(
            parameters=[
                OpenApiParameter(
                    "price",
                    type={"type": "list", "items": {"type": "number"}},
                ),
                OpenApiParameter(
                    "category",
                    type={"type": "list", "items": {"type": "number"}},
                )
            ]
        )
        def list(self, request, *args, **kwargs):
            return super().list(request, *args, **kwargs)

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

    @method_decorator(cache_page(10))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all().order_by("id")
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]

    def get_queryset(self):
        """Получаем корзину только текущего пользователя."""
        user_id = self.request.user.id
        return Cart.objects.filter(user_id=user_id).order_by("id")

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)
        with transaction.atomic():
            cart = serializer.save()
            product = cart.items
            if product.inventory < cart.quantity:
                raise ValidationError("Not enough stock.")
            product.inventory -= cart.quantity
            product.save()

    def perform_update(self, serializer):
        with transaction.atomic():
            cart = serializer.save()
            product = cart.items
            old_quantity = self.get_object().quantity
            new_quantity = cart.quantity
            quantity_diff = new_quantity - old_quantity
            if product.inventory < quantity_diff:
                raise ValidationError("Not enough stock.")
            product.inventory -= quantity_diff
            product.save()


class UserInfoView(APIView):
    authentication_classes = [MicroserviceJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(request.user.user_data, status=status.HTTP_200_OK)
