from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.checklists.models import COMPANIES, Checklist


class Optional(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    parent_checklist = models.ForeignKey(
        Checklist,
        verbose_name=_("Parent Checklist"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    process_number = models.CharField(_("Process Number"), max_length=10)
    company = models.CharField(_("Company"), choices=COMPANIES, default="Gimi", max_length=4)
    extended_warranty = models.BooleanField(_("Extended Warranty"))

    def __str__(self):
        return f"{self.company}-{self.process_number} | {self.extended_warranty}"
