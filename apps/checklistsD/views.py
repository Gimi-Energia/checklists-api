from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import ChecklistD
from .serializers import ChecklistDReadSerializer, ChecklistDWriteSerializer


class ChecklistDViewSet(viewsets.ModelViewSet):
    queryset = ChecklistD.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ChecklistDReadSerializer
        return ChecklistDWriteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            transformers_count = len(request.data.get("transformers", []))
            transformers_quantity = serializer.validated_data["transformers_quantity"]

            if transformers_quantity != transformers_count:
                return Response(
                    {
                        "error": f"Quantidade de transformadores ({transformers_quantity}) não corresponde à contagem ({transformers_count})."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
