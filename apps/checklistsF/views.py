from rest_framework import viewsets

from .models import ChecklistF
from .serializers import ChecklistFSerializer


class ChecklistFViewSet(viewsets.ModelViewSet):
    queryset = ChecklistF.objects.all()
    serializer_class = ChecklistFSerializer
