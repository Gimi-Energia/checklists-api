from rest_framework import serializers

from .models import ChecklistE
from .services.email_service import send_registration_email


class ChecklistESerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistE
        fields = "__all__"

    def create(self, validated_data):
        checklist = ChecklistE.objects.create(**validated_data)

        send_registration_email(checklist)

        return checklist
