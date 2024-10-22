from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import ChecklistB
from .serializers import ChecklistBReadSerializer, ChecklistBWriteSerializer


class ChecklistBViewSet(viewsets.ModelViewSet):
    queryset = ChecklistB.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["created_at"]
    filterset_fields = ["parent_checklist__id", "process_number", "item", "company"]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ChecklistBReadSerializer
        return ChecklistBWriteSerializer
