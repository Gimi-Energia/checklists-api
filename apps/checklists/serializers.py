from django.conf import settings
from django.core.mail import send_mail
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
        products_data = validated_data.pop("checklistproduct_set", [])
        checklist = Checklist.objects.create(**validated_data)
        for product_data in products_data:
            product = Product.objects.get(id=product_data["product"]["id"])
            ChecklistProduct.objects.create(
                checklist=checklist, product=product, status=product_data["status"]
            )

        subject = "Grupo Gimi - Novo Checklist Criado"
        message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    font-size: 16px;
                }}
                .btn {{
                    display: inline-block;
                    background-color: #f0f0f0;
                    padding: 8px 16px;
                    text-align: center;
                    text-decoration: none;
                    font-size: 16px;
                    border-radius: 10px;
                    margin-top: 10px;
                    border: 2px solid black;
                    font-weight: bold;
                }}
                .code {{
                    background-color: #f0f0f0;
                    padding: 2px 4px;
                    border-radius: 4px;
                    font-family: monospace;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <p>Olá <strong>{checklist.client_name}</strong>!</p>
            <p>Um novo checklist do Grupo Gimi foi enviado. 🎉</p>
            <p>Insira o ID <span class="code">{checklist.id}</span> em nosso webapp para prosseguir.</p>
            <a href="https://www.google.com/" target="_blank" class="btn">Acessar Webapp</a>
        </body>
        </html>
        """
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [checklist.client_email]
        send_mail(
            subject=subject,
            message=f"Cole o ID: {checklist.id} em nosso webapp",
            from_email=email_from,
            recipient_list=recipient_list,
            html_message=message,
            fail_silently=False,
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
