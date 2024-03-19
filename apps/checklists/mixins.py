from rest_framework import status as http_status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ChecklistProduct, Product


class ProductActionsMixin:
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

            quantity = product_data.get("quantity", "")
            items_numbers = product_data.get("items_numbers", [])
            items_answered = product_data.get("items_answered", [])

            if quantity != len(items_numbers):
                return Response(
                    {"error": "Quantity and the length of items_numbers must be equal."},
                    status=http_status.HTTP_400_BAD_REQUEST,
                )

            ChecklistProduct.objects.create(
                checklist=checklist,
                product=product,
                quantity=quantity,
                items_numbers=items_numbers,
                items_answered=items_answered,
            )

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

            try:
                checklist_product = ChecklistProduct.objects.get(
                    checklist=checklist, product=product
                )
                new_quantity = product_data.get("quantity", checklist_product.quantity)
                new_items_numbers = product_data.get(
                    "items_numbers", checklist_product.items_numbers
                )
                new_items_answered = product_data.get(
                    "items_answered", checklist_product.items_answered
                )

            except ChecklistProduct.DoesNotExist:
                return Response(
                    {"error": f"Product with ID '{product_id}' is not on the checklist."},
                    status=http_status.HTTP_404_NOT_FOUND,
                )

            if new_quantity is not None and len(new_items_numbers) != new_quantity:
                return Response(
                    {"error": "Quantity and the length of items must be equal."},
                    status=http_status.HTTP_400_BAD_REQUEST,
                )

            if new_quantity is not None:
                checklist_product.quantity = new_quantity
                updates_made = True
            if new_items_numbers is not None:
                checklist_product.items_numbers = new_items_numbers
                updates_made = True
            if new_items_answered is not None:
                checklist_product.items_answered = new_items_answered
                updates_made = True
            if updates_made:
                checklist_product.save()

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

    @action(detail=True, methods=["patch"])
    def register_answer(self, request, pk=None):
        checklist = self.get_object()
        product_id = request.data.get("product_id")
        item = request.data.get("item")

        try:
            checklist_product = ChecklistProduct.objects.get(
                checklist=checklist, product__id=product_id
            )
        except ChecklistProduct.DoesNotExist:
            return Response(
                {"error": f"Product '{product_id}' not found in the checklist."},
                status=http_status.HTTP_404_NOT_FOUND,
            )

        if item not in checklist_product.items_numbers:
            return Response(
                {"error": f"The item '{item}' is not valid for this product."},
                status=http_status.HTTP_400_BAD_REQUEST,
            )

        if item in checklist_product.items_answered:
            return Response(
                {"error": f"The item '{item}' has already been answered."},
                status=http_status.HTTP_400_BAD_REQUEST,
            )

        if len(checklist_product.items_answered) >= checklist_product.quantity:
            return Response(
                {"error": "The number of answered items cannot exceed the product quantity."},
                status=http_status.HTTP_400_BAD_REQUEST,
            )

        checklist_product.items_answered.append(item)
        checklist_product.save()

        return Response(
            {"success": f"Item '{item}' successfully registered."}, status=http_status.HTTP_200_OK
        )
