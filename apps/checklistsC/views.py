from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import ChecklistC
from .serializers import ChecklistCSerializer


class ChecklistCViewSet(viewsets.ModelViewSet):
    queryset = ChecklistC.objects.all()
    serializer_class = ChecklistCSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            transformers_count = len(request.data.get("transformers", []))
            current_transformers_count = len(request.data.get("current_transformers", []))

            if serializer.validated_data["measurements_consumers_quantity"] != transformers_count:
                return Response(
                    {
                        "error": "Measurements/Consumers quantity do not match their respective count."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if (
                current_transformers_count > 0
                and serializer.validated_data["breakers_quantity"] != current_transformers_count
            ):
                return Response(
                    {"error": "Breakers quantity do not match their respective count."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
