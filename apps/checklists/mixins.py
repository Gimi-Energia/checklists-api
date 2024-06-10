from rest_framework import status as http_status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ChecklistProduct


class ProductActionsMixin:
    @action(detail=True, methods=["patch"])
    def register_answer(self, request, pk=None):
        checklist = self.get_object()
        product_id = request.data.get("product_id")
        item = request.data.get("item")

        try:
            checklist_product = ChecklistProduct.objects.get(
                checklist=checklist, product__id=product_id, item=item
            )
        except ChecklistProduct.DoesNotExist:
            return Response(
                {"error": f"item '{item}' or checklist '{product_id}' not found."},
                status=http_status.HTTP_404_NOT_FOUND,
            )

        if checklist_product.is_answered:
            return Response(
                {"error": f"item '{item}' of checklist '{product_id}' has already been answered."},
                status=http_status.HTTP_400_BAD_REQUEST,
            )

        checklist_product.is_answered = True
        checklist_product.save()

        return Response(
            {"success": f"item '{item}' of product '{product_id}' successfully registered."},
            status=http_status.HTTP_200_OK,
        )
