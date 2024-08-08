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
    coord_selectivity = models.BooleanField(_("Coord Selectivity"), default=False)
    relay_parameterization = models.BooleanField(_("Relay Parameterization"), default=False)
    relay_commissioning = models.BooleanField(_("Relay Commissioning"), default=False)
    panel_commissioning = models.BooleanField(_("Panel Commissioning"), default=False)
    busbar_installation = models.BooleanField(_("Busbar Installation"), default=False)
    protection_equipment = models.BooleanField(_("Protection Equipment"), default=False)

    def __str__(self):
        return f"{self.company}-{self.process_number}"
