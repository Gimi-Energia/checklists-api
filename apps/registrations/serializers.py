from rest_framework import serializers

from .models import Registration
from utils.validators.custom_validators import valid_cnpj, valid_cep


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
