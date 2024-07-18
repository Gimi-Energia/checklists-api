from django.db import transaction
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
        fields = ["product_id", "item", "is_answered"]


class ChecklistSerializer(serializers.ModelSerializer):
    products = ChecklistProductSerializer(source="checklistproduct_set", many=True)

    class Meta:
        model = Checklist
        fields = "__all__"

    def create(self, validated_data):
        products_data = validated_data.pop("checklistproduct_set", [])

        with transaction.atomic():
            checklist = Checklist.objects.create(**validated_data)

            existing_products = set()
            for product_data in products_data:
                product_id = product_data["product"]["id"]
                item = product_data.get("item")

                if (product_id, item) in existing_products:
                    raise serializers.ValidationError(
                        {
                            "Error": f"Duplicate product {product_id} with item {item} in the same request."
                        }
                    )

                existing_products.add((product_id, item))

                product = Product.objects.get(id=product_id)
                is_answered = product_data.get("is_answered")

                ChecklistProduct.objects.create(
                    checklist=checklist,
                    product=product,
                    item=item,
                    is_answered=is_answered,
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
            if "item" in product_data:
                defaults["item"] = product_data["item"]
            if "is_answered" in product_data:
                defaults["is_answered"] = product_data["is_answered"]

            checklist_product, created = ChecklistProduct.objects.update_or_create(
                checklist=instance, product=product, defaults=defaults
            )

        return instance
