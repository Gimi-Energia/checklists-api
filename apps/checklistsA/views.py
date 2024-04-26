from rest_framework import viewsets
from .models import ChecklistA
from .serializers import ChecklistASerializer


class ChecklistAViewSet(viewsets.ModelViewSet):
    queryset = ChecklistA.objects.all()
    serializer_class = ChecklistASerializer
