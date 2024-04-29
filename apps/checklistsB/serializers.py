from rest_framework import serializers

from .models import ChecklistB
from .services.email_service import send_registration_email


class ChecklistBSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistB
        fields = "__all__"

    def create(self, validated_data):
        checklist = ChecklistB.objects.create(**validated_data)

        send_registration_email(checklist)

        return checklist
