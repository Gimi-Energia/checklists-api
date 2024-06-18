from uuid import uuid4

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.users.models import User

COMPANIES = [
    ("Gimi", "Gimi"),
    ("GBL", "GBL"),
    ("GPB", "GPB"),
    ("GS", "GS"),
    ("GIR", "GIR"),
]


class Product(models.Model):
    id = models.CharField(primary_key=True, max_length=4, unique=True)
    name = models.CharField(_("Product Name"), max_length=50)

    def __str__(self):
        return f"Checklist {self.id} - {self.name}"


class Checklist(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    user = models.ForeignKey(
        User, verbose_name=_("User"), on_delete=models.CASCADE, null=True, blank=True
    )
    company = models.CharField(_("Company"), choices=COMPANIES, default="Gimi", max_length=4)
    budget_number = models.CharField(_("Budget Number"), max_length=10)
    client_name = models.CharField(_("Client Name"), max_length=120)
    client_email = models.EmailField(_("Cliente Email"), max_length=254)
    products = models.ManyToManyField(Product, through="ChecklistProduct", null=True, blank=True)
    answered_registration = models.BooleanField(_("Answered Registration"), default=False)
    answered_optional = models.BooleanField(_("Answered Optional"), default=False)
    created_at = models.DateTimeField(_("Created At"), default=timezone.now)

    def __str__(self):
        return f"{self.company} - {self.budget_number}"


class ChecklistProduct(models.Model):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    item = models.CharField(_("Item"), max_length=3, default="1")
    is_answered = models.BooleanField(_("Answered"), default=False)

    def __str__(self):
        return f"{self.checklist} - {self.product}"
