from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

COMPANIES = [
    ("Gimi", "Gimi"),
    ("GBL", "GBL"),
    ("GPB", "GPB"),
    ("GS", "GS"),
    ("GIR", "GIR"),
]


class BaseModel(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(_("Creation Date"), blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(_("Update Date"), blank=True, null=True, auto_now=True)
    process_number = models.CharField(_("Process Number"), max_length=10)
    company = models.CharField(_("Company"), choices=COMPANIES, default="Gimi", max_length=4)
