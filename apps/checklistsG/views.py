from rest_framework import viewsets

from .models import ChecklistG
from .serializers import ChecklistGReadSerializer, ChecklistGWriteSerializer


class ChecklistGViewSet(viewsets.ModelViewSet):
    queryset = ChecklistG.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ChecklistGReadSerializer
        return ChecklistGWriteSerializer
