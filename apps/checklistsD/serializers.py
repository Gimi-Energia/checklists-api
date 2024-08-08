from django.db import transaction
from rest_framework import serializers

from apps.checklists.serializers import ChecklistCustomSerializer

from .models import ChecklistD, Transformer
from .services.email_service import send_checklist_email


class TransformerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transformer
        fields = ["power"]
        ref_name = "TransformerChecklistD"


class ChecklistDWriteSerializer(serializers.ModelSerializer):
    transformers = TransformerSerializer(many=True)

    class Meta:
        model = ChecklistD
        fields = "__all__"

    def create(self, validated_data):
        transformers_data = validated_data.pop("transformers")

        with transaction.atomic():
            checklist = ChecklistD.objects.create(**validated_data)

            for transformer_data in transformers_data:
                Transformer.objects.create(checklist=checklist, **transformer_data)

            send_checklist_email(checklist, transformers_data)

        return checklist


class ChecklistDReadSerializer(serializers.ModelSerializer):
    parent_checklist = ChecklistCustomSerializer()
    transformers = TransformerSerializer(many=True)

    class Meta:
        model = ChecklistD
        fields = "__all__"
