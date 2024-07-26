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
            consumers_quantity = serializer.validated_data.get("measurements_consumers_quantity")
            consumers = request.data.get("consumers", [])

            if consumers_quantity != len(consumers):
                return Response(
                    {
                        "error": f"Consumers quantity ({consumers_quantity}) does not match the count ({len(consumers)})."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            for index, substation in enumerate(consumers):
                expected_transformers = substation.get("transformers_quantity", 0)
                actual_transformers = len(substation.get("transformers", []))

                if expected_transformers != actual_transformers:
                    return Response(
                        {
                            "error": f"Consumer {index + 1}: transformers quantity ({expected_transformers}) does not match the count ({actual_transformers})."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            breakers_quantity = serializer.validated_data.get("breakers_quantity") + 1
            current_transformers_count = len(request.data.get("current_transformers", []))

            if current_transformers_count > 0 and breakers_quantity != current_transformers_count:
                return Response(
                    {
                        "error": f"Breakers quantity ({breakers_quantity}) does not match the count ({current_transformers_count})."
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
                    {"error": "If study is Gimi, send the needed fields."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not serializer.validated_data["gimi_study"] and not (
                serializer.validated_data.get("have_study", False)
                or serializer.validated_data.get("study_prediction", False)
                or current_transformers_count == 0
            ):
                return Response(
                    {"error": "If study is Client, send the study fields."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
