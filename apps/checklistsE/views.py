from rest_framework import viewsets

from .models import ChecklistE
from .serializers import ChecklistEReadSerializer, ChecklistEWriteSerializer


class ChecklistEViewSet(viewsets.ModelViewSet):
    queryset = ChecklistE.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ChecklistEReadSerializer
        return ChecklistEWriteSerializer
