from django.db import transaction
from rest_framework import serializers

from .models import ChecklistG
from .services.email_service import send_checklist_email


class ChecklistGSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistG
        fields = "__all__"

    def create(self, validated_data):
        with transaction.atomic():
            checklist = ChecklistG.objects.create(**validated_data)

            send_checklist_email(checklist)

        return checklist
