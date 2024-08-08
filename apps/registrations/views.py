from rest_framework import viewsets

from .models import Registration
from .serializers import RegistrationReadSerializer, RegistrationWriteSerializer


class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RegistrationReadSerializer
        return RegistrationWriteSerializer
