from rest_framework import viewsets

from .models import ChecklistB
from .serializers import ChecklistBSerializer


class ChecklistBViewSet(viewsets.ModelViewSet):
    queryset = ChecklistB.objects.all()
    serializer_class = ChecklistBSerializer
