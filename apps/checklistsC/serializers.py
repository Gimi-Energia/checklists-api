from django.db import transaction
from rest_framework import serializers

from apps.checklists.serializers import ChecklistCustomSerializer

from .models import ChecklistC, Consumer, CurrentTransformer, Transformer
from .services.email_service import send_checklist_email


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


class ConsumerSerializer(serializers.ModelSerializer):
    transformers = TransformerSerializer(many=True)

    class Meta:
        model = Consumer
        fields = ["transformers_quantity", "transformers"]


class ChecklistCWriteSerializer(serializers.ModelSerializer):
    consumers = ConsumerSerializer(many=True)
    current_transformers = CurrentTransformerSerializer(many=True, required=False)

    class Meta:
        model = ChecklistC
        fields = "__all__"

    def create(self, validated_data):
        consumers_data = validated_data.pop("consumers")
        current_transformers_data = validated_data.pop("current_transformers", None)

        if "measurements_consumers_quantity" not in validated_data:
            validated_data["measurements_consumers_quantity"] = 1

        with transaction.atomic():
            checklist = ChecklistC.objects.create(**validated_data)

            for consumer_data in consumers_data:
                transformers_data = consumer_data.pop("transformers")
                consumer = Consumer.objects.create(checklist=checklist, **consumer_data)

                for transformer_data in transformers_data:
                    Transformer.objects.create(consumer=consumer, **transformer_data)

            if current_transformers_data:
                for ct_data in current_transformers_data:
                    CurrentTransformer.objects.create(checklist=checklist, **ct_data)

            send_checklist_email(checklist)

        return checklist


class ChecklistCReadSerializer(serializers.ModelSerializer):
    parent_checklist = ChecklistCustomSerializer()
    consumers = ConsumerSerializer(many=True)
    current_transformers = CurrentTransformerSerializer(many=True, required=False)

    class Meta:
        model = ChecklistC
        fields = "__all__"
