from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import ChecklistC
from .serializers import ChecklistCReadSerializer, ChecklistCWriteSerializer


class ChecklistCViewSet(viewsets.ModelViewSet):
    queryset = ChecklistC.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ChecklistCReadSerializer
        return ChecklistCWriteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            consumers_quantity = serializer.validated_data.get("measurements_consumers_quantity")
            consumers = request.data.get("consumers", [])

            if consumers_quantity != len(consumers):
                return Response(
                    {
                        "error": f"Quantiade de Medição/Consumidores ({consumers_quantity}) não corresponde à contagem ({len(consumers)})."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            for index, substation in enumerate(consumers):
                expected_transformers = substation.get("transformers_quantity", 0)
                actual_transformers = len(substation.get("transformers", []))

                if expected_transformers != actual_transformers:
                    return Response(
                        {
                            "error": f"Medição/Consumidor {index + 1}: quantidade de transformadores ({expected_transformers}) não corresponde à contagem ({actual_transformers})."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            breakers_quantity = serializer.validated_data.get("breakers_quantity") + 1
            current_transformers_count = len(request.data.get("current_transformers", []))

            if current_transformers_count == 0:
                current_transformers_count = 1

            if breakers_quantity != current_transformers_count:
                return Response(
                    {
                        "error": f"Quantidade de TCs ({breakers_quantity}) não corresponde à contagem ({current_transformers_count})."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if serializer.validated_data["fire_exit"] and not serializer.validated_data.get(
                "fire_transformer_power"
            ):
                return Response(
                    {"error": "Envie a potência do trafo de incêndio."},
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
