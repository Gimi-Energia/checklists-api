from rest_framework import serializers

from utils.validators.custom_validators import valid_cep, valid_cnpj

from .models import Registration
from .services.email_service import send_registration_email


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = "__all__"

    def validate(self, data):
        if not valid_cnpj(data["billing_cnpj"]):
            raise serializers.ValidationError({"billing_cpf": "Invalid CNPJ."})
        if not valid_cep(data["zip_code"]):
            raise serializers.ValidationError({"zip_code": "Invalid CEP."})

        return data

    def create(self, validated_data):
        registration = super().create(validated_data)

        send_registration_email(registration)

        return registration
