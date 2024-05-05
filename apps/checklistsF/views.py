from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import ChecklistF
from .serializers import ChecklistFSerializer


class ChecklistFViewSet(viewsets.ModelViewSet):
    queryset = ChecklistF.objects.all()
    serializer_class = ChecklistFSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            substations_quantity = serializer.validated_data.get("substations_quantity")
            substations = request.data.get("substations", [])

            if substations_quantity != len(substations):
                return Response(
                    {
                        "error": f"Substations quantity ({substations_quantity}) does not match the count ({len(substations)})."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            for index, substation in enumerate(substations):
                expected_transformers = substation.get("transformers_quantity", 0)
                actual_transformers = len(substation.get("transformers", []))

                if expected_transformers != actual_transformers:
                    return Response(
                        {
                            "error": f"Substation {index + 1}: transformers quantity ({expected_transformers}) does not match the count ({actual_transformers})."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            breakers_quantity = serializer.validated_data.get("breakers_quantity")
            current_transformers = request.data.get("current_transformers", [])

            if breakers_quantity != len(current_transformers):
                return Response(
                    {
                        "error": f"Breakers quantity ({breakers_quantity}) does not match the count ({len(current_transformers)})."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
