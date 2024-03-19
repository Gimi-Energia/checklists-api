from rest_framework import viewsets

from .mixins import ProductActionsMixin
from .models import Checklist, Product
from .serializers import ChecklistSerializer, ProductSerializer


class ChecklistViewSet(ProductActionsMixin, viewsets.ModelViewSet):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
