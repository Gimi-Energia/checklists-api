from rest_framework import status as http_status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Checklist, ChecklistProduct, Product
from .serializers import ChecklistSerializer, ProductSerializer


class ChecklistViewSet(viewsets.ModelViewSet):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer

    @action(detail=True, methods=["post"])
    def add_products(self, request, pk=None):
        checklist = self.get_object()
        products_data = request.data.get("products", [])
        seen_products = set()

        if not products_data:
            return Response(
                {"error": "No product specified for addition."},
                status=http_status.HTTP_400_BAD_REQUEST,
            )

        for product_data in products_data:
            product_id = product_data.get("product_id")

            if product_id in seen_products:
                return Response(
                    {"error": f"Duplicate product ID '{product_id}' in the request."},
                    status=http_status.HTTP_400_BAD_REQUEST,
                )
            seen_products.add(product_id)

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response(
                    {"error": f"Product with ID '{product_id}' does not exist."},
                    status=http_status.HTTP_404_NOT_FOUND,
                )

            if ChecklistProduct.objects.filter(checklist=checklist, product=product).exists():
                return Response(
                    {"error": f"Product with ID '{product_id}' is already added to the checklist."},
                    status=http_status.HTTP_400_BAD_REQUEST,
                )

            status = product_data.get("status", "")
            ChecklistProduct.objects.create(checklist=checklist, product=product, status=status)

        return Response(
            {"success": "Products successfully added."}, status=http_status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["patch"])
    def update_products(self, request, pk=None):
        checklist = self.get_object()
        products_data = request.data.get("products", [])
        updates_made = False

        if not products_data:
            return Response(
                {"error": "No product specified for update."},
                status=http_status.HTTP_400_BAD_REQUEST,
            )

        for product_data in products_data:
            product_id = product_data.get("product_id")

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response(
                    {"error": f"Product with ID '{product_id}' does not exist."},
                    status=http_status.HTTP_404_NOT_FOUND,
                )

            new_status = product_data.get("status")
            try:
                checklist_product = ChecklistProduct.objects.get(
                    checklist=checklist, product=product
                )
                if checklist_product.status != new_status:
                    checklist_product.status = new_status
                    checklist_product.save()
                    updates_made = True
            except ChecklistProduct.DoesNotExist:
                return Response(
                    {"error": f"Product with ID '{product_id}' is not on the checklist."},
                    status=http_status.HTTP_404_NOT_FOUND,
                )

        if updates_made:
            return Response(
                {"success": "Products successfully updated."}, status=http_status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "There are no products to update."},
                status=http_status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["delete"])
    def remove_products(self, request, pk=None):
        checklist = self.get_object()
        product_ids = request.data.get("products", [])

        if not product_ids:
            return Response(
                {"error": "No products specified for removal."},
                status=http_status.HTTP_400_BAD_REQUEST,
            )

        if len(product_ids) != len(set(product_ids)):
            return Response(
                {"error": "Duplicate product IDs in the request."},
                status=http_status.HTTP_400_BAD_REQUEST,
            )

        errors = []
        products_to_remove = []

        for product_id in product_ids:
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                errors.append(f"Product with ID '{product_id}' does not exist.")
                continue

            if not ChecklistProduct.objects.filter(checklist=checklist, product=product).exists():
                errors.append(f"Product with ID '{product_id}' is not on the checklist.")
                continue

            products_to_remove.append(product)

        if errors:
            return Response({"errors": errors}, status=http_status.HTTP_400_BAD_REQUEST)

        for product in products_to_remove:
            ChecklistProduct.objects.filter(checklist=checklist, product=product).delete()

        return Response(
            {"success": "Products successfully removed."}, status=http_status.HTTP_200_OK
        )


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
