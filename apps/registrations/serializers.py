from django.db import transaction
from rest_framework import serializers

from apps.checklists.serializers import ChecklistCustomSerializer
from utils.validators.custom_validators import valid_cnpj, valid_cpf

from .models import Registration
from .services.email_service import send_registration_email


class RegistrationWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = "__all__"

    def validate(self, data):
        if not valid_cpf(data["lr_document"]):
            raise serializers.ValidationError({"lr_document": "CPF inválido."})

        return data

    def create(self, validated_data):
        with transaction.atomic():
            registration = super().create(validated_data)

            send_registration_email(registration)

        return registration


class RegistrationReadSerializer(serializers.ModelSerializer):
    parent_checklist = ChecklistCustomSerializer()

    class Meta:
        model = Registration
        fields = "__all__"
