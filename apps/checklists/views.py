from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .mixins import ProductActionsMixin
from .models import Checklist, Product
from .serializers import ChecklistReadSerializer, ChecklistWriteSerializer, ProductSerializer


class ChecklistViewSet(ProductActionsMixin, viewsets.ModelViewSet):
    queryset = Checklist.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = [
        "company",
        "process_number",
        "auxiliary_number",
        "construction_name",
        "client_name",
        "client_email",
        "products__id",
        "user__email",
    ]
    ordering_fields = ["created_at"]
    filterset_fields = ["company", "process_number", "auxiliary_number"]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ChecklistReadSerializer
        return ChecklistWriteSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
