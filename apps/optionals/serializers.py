from django.db import transaction
from rest_framework import serializers

from apps.checklists.serializers import ChecklistCustomSerializer

from .models import Optional
from .services.email_service import send_optionals_email


class OptionalWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Optional
        fields = "__all__"

    def create(self, validated_data):
        with transaction.atomic():
            instance = super().create(validated_data)

            send_optionals_email(instance)

        return instance


class OptionalReadSerializer(serializers.ModelSerializer):
    parent_checklist = ChecklistCustomSerializer()

    class Meta:
        model = Optional
        fields = "__all__"
