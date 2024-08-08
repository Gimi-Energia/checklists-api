from rest_framework import viewsets

from .models import ChecklistB
from .serializers import ChecklistBReadSerializer, ChecklistBWriteSerializer


class ChecklistBViewSet(viewsets.ModelViewSet):
    queryset = ChecklistB.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ChecklistBReadSerializer
        return ChecklistBWriteSerializer
