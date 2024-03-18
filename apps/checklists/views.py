from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Checklist, ChecklistProduct, Product
from .serializers import ChecklistProductSerializer, ChecklistSerializer, ProductSerializer


class ChecklistViewSet(viewsets.ModelViewSet):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer

    @action(detail=True, methods=["post"])
    def add_product(self, request, pk=None):
        checklist = self.get_object()
        product_id = request.data.get("product_id")
        product_status = request.data.get("status", "")

        if ChecklistProduct.objects.filter(checklist=checklist, product_id=product_id).exists():
            return Response(
                {"error": "product already in checklist"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            product = Product.objects.get(pk=product_id)
            ChecklistProduct.objects.create(
                checklist=checklist, product=product, status=product_status
            )
            return Response({"success": "product added"}, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist:
            return Response({"error": "invalid product"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["patch"])
    def edit_product(self, request, pk=None):
        checklist = self.get_object()
        product_id = request.data.get("product_id")  # Este é o 'id' do Produto, que é uma string
        new_status = request.data.get("status")

        try:
            # Aqui assumimos que o modelo Produto usa um CharField ou UUIDField para o 'id'
            product = Product.objects.get(id=product_id)
            # Agora, obtemos o ChecklistProduct usando o produto e a checklist
            checklist_product = ChecklistProduct.objects.get(checklist=checklist, product=product)
            if new_status:
                checklist_product.status = new_status
                checklist_product.save()
                return Response(
                    {"status": "product status updated"}, status=status.HTTP_200_OK
                )
        except Product.DoesNotExist:
            return Response(
                {"status": "invalid product id"}, status=status.HTTP_400_BAD_REQUEST
            )
        except ChecklistProduct.DoesNotExist:
            return Response(
                {"status": "product not in checklist"}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=["delete"])
    def remove_product(self, request, pk=None):
        checklist = self.get_object()
        product_id = request.data.get("product_id")

        checklist_product = get_object_or_404(
            ChecklistProduct, checklist=checklist, product_id=product_id
        )
        checklist_product.delete()
        return Response({"success": "product removed"}, status=status.HTTP_204_NO_CONTENT)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
