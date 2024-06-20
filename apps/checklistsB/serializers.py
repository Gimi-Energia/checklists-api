from django.db import transaction
from rest_framework import serializers

from .models import ChecklistB
from .services.email_service import send_checklist_email


class ChecklistBSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistB
        fields = "__all__"

    def create(self, validated_data):
        with transaction.atomic():
            checklist = ChecklistB.objects.create(**validated_data)

            send_checklist_email(checklist)

        return checklist
