from django.db import transaction
from rest_framework import serializers

from apps.checklists.serializers import ChecklistCustomSerializer

from .models import ChecklistG
from .services.email_service import send_checklist_email


class ChecklistGWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistG
        fields = "__all__"

    def create(self, validated_data):
        with transaction.atomic():
            checklist = ChecklistG.objects.create(**validated_data)

            send_checklist_email(checklist)

        return checklist


class ChecklistGReadSerializer(serializers.ModelSerializer):
    parent_checklist = ChecklistCustomSerializer()

    class Meta:
        model = ChecklistG
        fields = "__all__"
