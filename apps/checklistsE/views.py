from rest_framework import viewsets

from .models import ChecklistE
from .serializers import ChecklistESerializer


class ChecklistEViewSet(viewsets.ModelViewSet):
    queryset = ChecklistE.objects.all()
    serializer_class = ChecklistESerializer
