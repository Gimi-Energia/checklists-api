from django.db import transaction
from rest_framework import serializers

from .models import ChecklistF, CurrentTransformer, Substation, Transformer
from .services.email_service import send_checklist_email


class TransformerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transformer
        fields = ["power", "impedance", "demand", "type"]
        ref_name = "TransformerChecklistF"


class CurrentTransformerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentTransformer
        fields = ["ratio", "accuracy"]
        ref_name = "CurrentTransformerChecklistF"


class SubstationSerializer(serializers.ModelSerializer):
    transformers = TransformerSerializer(many=True)

    class Meta:
        model = Substation
        fields = [
            "name",
            "primary_voltage",
            "panel_usage",
            "cable_side",
            "transformers_quantity",
            "transformers",
        ]


class ChecklistFSerializer(serializers.ModelSerializer):
    substations = SubstationSerializer(many=True)
    current_transformers = CurrentTransformerSerializer(many=True, required=False)

    class Meta:
        model = ChecklistF
        fields = "__all__"

    def create(self, validated_data):
        substations_data = validated_data.pop("substations")
        current_transformers_data = validated_data.pop("current_transformers", None)

        if "substations_quantity" not in validated_data:
            validated_data["substations_quantity"] = 1

        with transaction.atomic():
            checklist = ChecklistF.objects.create(**validated_data)

            for substation_data in substations_data:
                transformers_data = substation_data.pop("transformers")
                substation = Substation.objects.create(checklist=checklist, **substation_data)

                for transformer_data in transformers_data:
                    Transformer.objects.create(substation=substation, **transformer_data)

            if current_transformers_data:
                for ct_data in current_transformers_data:
                    CurrentTransformer.objects.create(checklist=checklist, **ct_data)

            send_checklist_email(checklist)

        return checklist
