from rest_framework import serializers

from .models import ChecklistD, Transformer
from .services.email_service import send_registration_email


class TransformerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transformer
        fields = ["power"]


class ChecklistDSerializer(serializers.ModelSerializer):
    transformers = TransformerSerializer(many=True)

    class Meta:
        model = ChecklistD
        fields = "__all__"

    def create(self, validated_data):
        transformers_data = validated_data.pop("transformers")
        checklist = ChecklistD.objects.create(**validated_data)

        for transformer_data in transformers_data:
            Transformer.objects.create(checklist=checklist, **transformer_data)

        send_registration_email(checklist)

        return checklist
