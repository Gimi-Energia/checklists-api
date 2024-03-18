from rest_framework import serializers

from .models import Checklist, ChecklistProduct, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ChecklistProductSerializer(serializers.ModelSerializer):
    product_id = serializers.CharField(source="product.id")

    class Meta:
        model = ChecklistProduct
        fields = ["product_id", "status"]


class ChecklistSerializer(serializers.ModelSerializer):
    products = ChecklistProductSerializer(source="checklistproduct_set", many=True)

    class Meta:
        model = Checklist
        fields = "__all__"

    def create(self, validated_data):
        products_data = validated_data.pop(
            "checklistproduct_set", []
        )
        checklist = Checklist.objects.create(**validated_data)
        for product_data in products_data:
            product = Product.objects.get(
                id=product_data["product"]["id"]
            )
            ChecklistProduct.objects.create(
                checklist=checklist, product=product, status=product_data["status"]
            )
        return checklist

    def update(self, instance, validated_data):
        products_data = validated_data.pop("checklistproduct_set", [])
        instance = super().update(instance, validated_data)

        for product_data in products_data:
            product_id = product_data.get("product", {}).get("id")
            status = product_data.get("status", "")
            product = Product.objects.get(id=product_id)

            checklist_product, created = ChecklistProduct.objects.update_or_create(
                checklist=instance, product=product, defaults={"status": status}
            )

        return instance
