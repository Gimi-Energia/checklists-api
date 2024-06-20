from django.db import transaction
from rest_framework import serializers

from .models import ChecklistE
from .services.email_service import send_checklist_email


class ChecklistESerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistE
        fields = "__all__"

    def create(self, validated_data):
        with transaction.atomic():
            checklist = ChecklistE.objects.create(**validated_data)

            send_checklist_email(checklist)

        return checklist
