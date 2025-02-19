from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.models import User
from utils.base_model import BaseModel

REPEATED = 1
NOT_SENT = 1
SENT = 2
ANSWERED = 3

ART_CHOICES = [
    (NOT_SENT, "NOT SENT"),
    (SENT, "SENT"),
    (ANSWERED, "ANSWERED"),
]

STATUS_CHOICES = [
    (REPEATED, "PREVIOUSLY SENT"),
    (SENT, "SENT"),
    (ANSWERED, "ANSWERED"),
]


class Product(models.Model):
    id = models.CharField(primary_key=True, max_length=1, unique=True)
    name = models.CharField(_("Product Name"), max_length=50)

    def __str__(self):
        return f"Checklist {self.id} - {self.name}"


class Checklist(BaseModel):
    user = models.ForeignKey(
        User, verbose_name=_("User"), on_delete=models.CASCADE, null=True, blank=True
    )
    client_name = models.CharField(_("Client Name"), max_length=120)
    client_email = models.TextField(_("Client Email"))
    products = models.ManyToManyField(Product, through="ChecklistProduct")
    registration_status = models.IntegerField(
        _("Answered Registration"), choices=STATUS_CHOICES, default=SENT
    )
    optional_status = models.IntegerField(
        _("Answered Optional"), choices=STATUS_CHOICES, default=SENT
    )
    art_status = models.IntegerField(_("ART Status"), choices=ART_CHOICES, default=NOT_SENT)

    def __str__(self):
        return f"{self.company} - {self.process_number}"


class ChecklistProduct(models.Model):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    item = models.CharField(_("Item"), max_length=3, default="1")
    is_answered = models.BooleanField(_("Answered"), default=False)

    def __str__(self):
        return f"{self.checklist} - {self.product}"
