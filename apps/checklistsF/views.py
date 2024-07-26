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
            transformers_count = len(request.data.get("transformers", []))
            current_transformers_count = len(request.data.get("current_transformers", []))

            if serializer.validated_data["transformers_quantity"] != transformers_count:
                return Response(
                    {"error": "Transformers quantity do not match their respective count."},
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
