from rest_framework import viewsets

from .models import ChecklistG
from .serializers import ChecklistGSerializer


class ChecklistGViewSet(viewsets.ModelViewSet):
    queryset = ChecklistG.objects.all()
    serializer_class = ChecklistGSerializer
