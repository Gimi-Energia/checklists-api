from rest_framework import serializers

from .models import Optional
from .services.email_service import send_optionals_email


class OptionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Optional
        fields = "__all__"

    def create(self, validated_data):
        instance = super().create(validated_data)

        send_optionals_email(instance)

        return instance
