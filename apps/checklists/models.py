from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

COMPANIES = [
    ("Gimi", "Gimi"),
    ("GBL", "GBL"),
    ("GPB", "GPB"),
    ("GS", "GS"),
    ("GIR", "GIR"),
    ("Group", "Group"),
]


class Product(models.Model):
    id = models.CharField(primary_key=True, max_length=1, unique=True)
    name = models.CharField(_("Product Name"), max_length=50)

    def __str__(self):
        return f"Checklist {self.id} - {self.name}"


class Checklist(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    company = models.CharField(_("Company"), choices=COMPANIES, default="Gimi", max_length=5)
    budget_number = models.CharField(_("Budget Number"), max_length=10)
    client_name = models.CharField(_("Client Name"), max_length=120)
    client_email = models.EmailField(_("Cliente Email"), max_length=254)
    products = models.ManyToManyField(Product, through="ChecklistProduct")

    def __str__(self):
        return self.budget_number


class ChecklistProduct(models.Model):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_("Quantity"))
    items_numbers = models.JSONField(_("Item Numbers"), default=list)
    items_answered = models.JSONField(_("Item Answered"), default=list)

    def __str__(self):
        return f"{self.checklist} - {self.produto}"
