from rest_framework import serializers

from utils.validators.custom_validators import valid_cnpj

from .models import Registration
from .services.email_service import send_registration_email


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = "__all__"

    def validate(self, data):
        if not valid_cnpj(data["billing_cnpj"]):
            raise serializers.ValidationError({"billing_cpf": "Invalid CNPJ."})

        return data

    def create(self, validated_data):
        registration = super().create(validated_data)

        send_registration_email(registration)

        return registration
