from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import ChecklistE
from .serializers import ChecklistEReadSerializer, ChecklistEWriteSerializer


class ChecklistEViewSet(viewsets.ModelViewSet):
    queryset = ChecklistE.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["created_at"]
    filterset_fields = ["parent_checklist__id", "process_number", "item", "company"]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ChecklistEReadSerializer
        return ChecklistEWriteSerializer
