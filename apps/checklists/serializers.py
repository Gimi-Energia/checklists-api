from rest_framework import serializers

from .models import Checklist, ChecklistProduct, Product
from .services.email_service import send_new_checklist_email


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ChecklistProductSerializer(serializers.ModelSerializer):
    product_id = serializers.CharField(source="product.id")

    class Meta:
        model = ChecklistProduct
        fields = ["product_id", "quantity", "items_numbers", "items_answered"]

    def validate(self, data):
        if "quantity" in data and "items_numbers" in data:
            if len(data["items_numbers"]) != data["quantity"]:
                raise serializers.ValidationError(
                    "The length of 'items_numbers' must be equal to 'quantity'."
                )
        return data


class ChecklistSerializer(serializers.ModelSerializer):
    products = ChecklistProductSerializer(source="checklistproduct_set", many=True)

    class Meta:
        model = Checklist
        fields = "__all__"

    def create(self, validated_data):
        products_data = validated_data.pop("checklistproduct_set", [])
        checklist = Checklist.objects.create(**validated_data)

        for product_data in products_data:
            product = Product.objects.get(id=product_data["product"]["id"])
            quantity = product_data.get("quantity")
            items_numbers = product_data.get("items_numbers", [])

            ChecklistProduct.objects.create(
                checklist=checklist,
                product=product,
                quantity=quantity,
                items_numbers=items_numbers,
            )

        send_new_checklist_email(checklist)
        return checklist

    def update(self, instance, validated_data):
        products_data = validated_data.pop("checklistproduct_set", [])
        instance = super().update(instance, validated_data)

        for product_data in products_data:
            product_id = product_data.get("product", {}).get("id")
            product = Product.objects.get(id=product_id)

            defaults = {}
            if "quantity" in product_data:
                defaults["quantity"] = product_data["quantity"]
            if "items_numbers" in product_data:
                defaults["items_numbers"] = product_data["items_numbers"]
            if "items_answered" in product_data:
                defaults["items_answered"] = product_data["items_answered"]

            checklist_product, created = ChecklistProduct.objects.update_or_create(
                checklist=instance, product=product, defaults=defaults
            )

        return instance
