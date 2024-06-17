from rest_framework import viewsets

from .models import Optional
from .serializers import OptionalSerializer


class OptionalViewSet(viewsets.ModelViewSet):
    queryset = Optional.objects.all()
    serializer_class = OptionalSerializer
