from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.checklists.models import Checklist
from utils.base_model import BaseModel

CONCESSIONAIRE_CHOICES = [
    ("ENEL-SP", "ENEL-SP"),
]

TYPE_CHOICES = [("Air", "Air"), ("Oil", "Oil")]


class ChecklistD(BaseModel):
    parent_checklist = models.ForeignKey(
        Checklist,
        verbose_name=_("Parent Checklist"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    item = models.CharField(_("Item"), max_length=3, default="1")
    concessionaire = models.CharField(
        max_length=20, choices=CONCESSIONAIRE_CHOICES, null=True, blank=True
    )
    other_concessionaire = models.CharField(max_length=20, null=True, blank=True)
    rated_voltage = models.CharField(_("Rated Voltage"), max_length=20)
    transformers_quantity = models.PositiveIntegerField(_("Transformers Quantity"))

    contractor_name = models.CharField(_("Contractor Name"), max_length=70)
    contractor_document = models.CharField(_("Contractor Document"), max_length=18)
    contractor_contact = models.CharField(_("Contractor Contact"), max_length=70)
    contractor_phone = models.CharField(_("Contractor Phone"), max_length=15)
    contractor_street = models.CharField(_("Contractor Street"), max_length=255)
    contractor_number = models.CharField(_("Contractor Number"), max_length=20)
    contractor_complement = models.CharField(
        _("Contractor Complement"), max_length=255, blank=True, null=True
    )
    contractor_neighborhood = models.CharField(_("Contractor Neighborhood"), max_length=100)
    contractor_city = models.CharField(_("Contractor City"), max_length=100)
    contractor_state = models.CharField(_("Contractor State"), max_length=50)
    contractor_zip_code = models.CharField(
        _("Contractor Zip Code"), max_length=10, blank=True, null=True
    )
    contractor_latitude = models.FloatField(_("Contractor Latitude"), blank=True, null=True)
    contractor_longitude = models.FloatField(_("Contractor Longitude"), blank=True, null=True)

    owner_name = models.CharField(_("Owner Name"), max_length=70)
    owner_document = models.CharField(_("Owner Document"), max_length=18)
    owner_contact = models.CharField(_("Owner Contact"), max_length=70)
    owner_phone = models.CharField(_("Owner Phone"), max_length=15)
    work_street = models.CharField(_("Work Street"), max_length=255)
    work_number = models.CharField(_("Work Number"), max_length=20)
    work_complement = models.CharField(_("Work Complement"), max_length=255, blank=True, null=True)
    work_neighborhood = models.CharField(_("Work Neighborhood"), max_length=100)
    work_city = models.CharField(_("Work City"), max_length=100)
    work_state = models.CharField(_("Work State"), max_length=50)
    work_zip_code = models.CharField(_("Work Zip Code"), max_length=10, blank=True, null=True)
    work_latitude = models.FloatField(_("Work Latitude"), blank=True, null=True)
    work_longitude = models.FloatField(_("Work Longitude"), blank=True, null=True)


class Transformer(models.Model):
    checklist = models.ForeignKey(ChecklistD, on_delete=models.CASCADE, related_name="transformers")
    power = models.FloatField(_("Transformer Power"))
