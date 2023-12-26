from rest_framework import viewsets, mixins
from shop.serializers import ProductSerializer
from shop.models import Product


class ProductViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
