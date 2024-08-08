from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.checklists.models import Checklist
from utils.base_model import BaseModel


class Optional(BaseModel):
    parent_checklist = models.ForeignKey(
        Checklist,
        verbose_name=_("Parent Checklist"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    extended_warranty = models.BooleanField(_("Extended Warranty"))

    def __str__(self):
        return f"{self.company}-{self.process_number} | {self.extended_warranty}"
