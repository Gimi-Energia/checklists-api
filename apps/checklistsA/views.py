from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import ChecklistA
from .serializers import ChecklistAReadSerializer, ChecklistAWriteSerializer


class ChecklistAViewSet(viewsets.ModelViewSet):
    queryset = ChecklistA.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ChecklistAReadSerializer
        return ChecklistAWriteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            transformers_count = len(request.data.get("transformers", []))
            current_transformers_count = len(request.data.get("current_transformers", []))
            transformers_quantity = serializer.validated_data["transformers_quantity"]
            breakers_quantity = serializer.validated_data["breakers_quantity"]

            if transformers_quantity != transformers_count:
                return Response(
                    {
                        "error": f"Quantidade de transformadores ({transformers_quantity}) não corresponde à contagem ({transformers_count})."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if current_transformers_count > 0 and breakers_quantity != current_transformers_count:
                return Response(
                    {
                        "error": f"Quantidade de TCs ({breakers_quantity}) não corresponde à contagem ({current_transformers_count})."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if serializer.validated_data["gimi_study"] and not (
                serializer.validated_data.get("icc3f", False)
                or serializer.validated_data.get("icc2f", False)
                or serializer.validated_data.get("iccftmax", False)
                or serializer.validated_data.get("iccftmin", False)
            ):
                return Response(
                    {"error": "Se o estudo for Gimi, envie os campos necessários."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not serializer.validated_data["gimi_study"] and not (
                serializer.validated_data.get("have_study", False)
                or serializer.validated_data.get("study_prediction", False)
                or current_transformers_count == 0
            ):
                return Response(
                    {"error": "Se o estudo for Cliente, envie os campos necessários."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
