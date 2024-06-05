from rest_framework import serializers

from .models import ChecklistC, CurrentTransformer, Transformer
from .services.email_service import send_registration_email


class TransformerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transformer
        fields = ["power", "impedance", "demand", "type"]
        ref_name = "TransformerChecklistC"


class CurrentTransformerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentTransformer
        fields = ["ratio", "accuracy"]
        ref_name = "CurrentTransformerChecklistC"


class ChecklistCSerializer(serializers.ModelSerializer):
    transformers = TransformerSerializer(many=True)
    current_transformers = CurrentTransformerSerializer(many=True, required=False)

    class Meta:
        model = ChecklistC
        fields = "__all__"

    def create(self, validated_data):
        transformers_data = validated_data.pop("transformers")
        current_transformers_data = validated_data.pop("current_transformers", None)
        checklist = ChecklistC.objects.create(**validated_data)

        for transformer_data in transformers_data:
            Transformer.objects.create(checklist=checklist, **transformer_data)

        if current_transformers_data:
            for ct_data in current_transformers_data:
                CurrentTransformer.objects.create(checklist=checklist, **ct_data)

        send_registration_email(checklist)

        return checklist
