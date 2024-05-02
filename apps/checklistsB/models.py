from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.checklists.models import COMPANIES, Checklist

CONCESSIONAIRE_CHOICES = [
    ("CPFL", "CPFL"),
    ("EDP_SP", "EDP-SP"),
    ("EDP_ES", "EDP-ES"),
    ("ELEKTRO", "ELEKTRO"),
]

PANEL_USAGE_CHOICES = [("Sheltered", "Sheltered"), ("Unsheltered", ("Unsheltered"))]

CABLE_SIDE_CHOICES = [("Left", "Left"), ("Right", "Right")]

TRANSFORMERS_CHOICES = [
    ("Dried", "Dried"),
    ("Mineral Oil", "Mineral Oil"),
    ("Vegetable Oil", "Vegetable Oil"),
]


class ChecklistB(models.Model):
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
    concessionaire = models.CharField(
        max_length=20, choices=CONCESSIONAIRE_CHOICES, default="CEEE", null=True, blank=True
    )
    other_concessionaire = models.CharField(max_length=20, null=True, blank=True)
    primary_voltage = models.FloatField(_("Primary Voltage (kV)"))
    secondary_voltage = models.CharField(_("Secondary Voltage"), max_length=20)
    panel_usage = models.CharField(
        _("Panel Usage"), max_length=20, choices=PANEL_USAGE_CHOICES, default="Sheltered"
    )
    contracted_demand = models.CharField(_("Contracted Demand"), max_length=8)
    transformer_type = models.CharField(
        _("Transformer Type"), choices=TRANSFORMERS_CHOICES, max_length=15
    )
    transformer_power = models.FloatField(_("Transformer Power"))
    manufacturer_project = models.BooleanField(_("Has a Manufacturer and Project?"), default=True)

    contractor_name = models.CharField(_("Contractor Name"), max_length=50)
    contractor_document = models.CharField(_("Contractor Document"), max_length=18)
    contractor_contact = models.CharField(_("Contractor Contact"), max_length=50)
    contractor_phone = models.CharField(_("Contractor Phone"), max_length=13)
    contractor_street = models.CharField(_("Contractor Street"), max_length=255)
    contractor_number = models.CharField(_("Contractor Number"), max_length=20)
    contractor_complement = models.CharField(
        _("Contractor Complement"), max_length=255, blank=True, null=True
    )
    contractor_neighborhood = models.CharField(_("Contractor Neighborhood"), max_length=100)
    contractor_city = models.CharField(_("Contractor City"), max_length=100)
    contractor_state = models.CharField(_("Contractor State"), max_length=50)
    contractor_zip_code = models.CharField(_("Contractor Zip Code"), max_length=20)

    owner_name = models.CharField(_("Owner Name"), max_length=50)
    owner_document = models.CharField(_("Owner Document"), max_length=18)
    owner_contact = models.CharField(_("Owner Contact"), max_length=50)
    owner_phone = models.CharField(_("Owner Phone"), max_length=13)
    work_street = models.CharField(_("Work Street"), max_length=255)
    work_number = models.CharField(_("Work Number"), max_length=20)
    work_complement = models.CharField(_("Work Complement"), max_length=255, blank=True, null=True)
    work_neighborhood = models.CharField(_("Work Neighborhood"), max_length=100)
    work_city = models.CharField(_("Work City"), max_length=100)
    work_state = models.CharField(_("Work State"), max_length=50)
    work_zip_code = models.CharField(_("Work Zip Code"), max_length=20)