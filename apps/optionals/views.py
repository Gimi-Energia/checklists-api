from rest_framework import viewsets

from .models import Optional
from .serializers import OptionalReadSerializer, OptionalWriteSerializer


class OptionalViewSet(viewsets.ModelViewSet):
    queryset = Optional.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return OptionalReadSerializer
        return OptionalWriteSerializer
