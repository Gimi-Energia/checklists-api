from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .mixins import ProductActionsMixin
from .models import Checklist, Product
from .serializers import ChecklistSerializer, ProductSerializer


class ChecklistViewSet(ProductActionsMixin, viewsets.ModelViewSet):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["company", "budget_number", "client_name", "client_email"]
    filterset_fields = ["company", "budget_number"]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
