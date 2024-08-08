from django.db import transaction
from rest_framework import serializers

from apps.checklists.serializers import ChecklistCustomSerializer

from .models import ChecklistB
from .services.email_service import send_checklist_email


class ChecklistBWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistB
        fields = "__all__"

    def create(self, validated_data):
        with transaction.atomic():
            checklist = ChecklistB.objects.create(**validated_data)

            send_checklist_email(checklist)

        return checklist


class ChecklistBReadSerializer(serializers.ModelSerializer):
    parent_checklist = ChecklistCustomSerializer()

    class Meta:
        model = ChecklistB
        fields = "__all__"
