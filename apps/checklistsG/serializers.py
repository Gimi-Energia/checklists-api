from rest_framework import serializers

from .models import ChecklistG
from .services.email_service import send_registration_email


class ChecklistGSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistG
        fields = "__all__"

    def create(self, validated_data):
        checklist = ChecklistG.objects.create(**validated_data)

        send_registration_email(checklist)

        return checklist
