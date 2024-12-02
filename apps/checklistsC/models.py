from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.checklists.models import Checklist
from utils.base_model import BaseModel

CONCESSIONAIRE_CHOICES = [
    ("CEEE", "CEEE"),
    ("CELESC", "CELESC"),
    ("CEMIG", "CEMIG"),
    ("CERIPA", "CERIPA"),
    ("COELBA", "COELBA"),
    ("CPFL", "CPFL"),
    ("EDP-SP", "EDP-SP"),
    ("EDP-ES", "EDP-ES"),
    ("ELEKTRO", "ELEKTRO"),
    ("ENEL", "ENEL"),
    ("ENERGISA", "ENERGISA"),
    ("EQUATORIAL", "EQUATORIAL"),
    ("LIGHT", "LIGHT"),
]

PANEL_USAGE_CHOICES = [("Sheltered", "Sheltered"), ("Unsheltered", ("Unsheltered"))]

CABLE_SIDE_CHOICES = [("Left", "Left"), ("Right", "Right")]

TYPE_CHOICES = [("Air", "Air"), ("Oil", "Oil")]


class ChecklistC(BaseModel):
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
    primary_voltage = models.FloatField(_("Primary Voltage (kV)"))
    panel_usage = models.CharField(
        _("Panel Usage"), max_length=20, choices=PANEL_USAGE_CHOICES, default="Sheltered"
    )
    cable_side = models.CharField(
        _("Cable Side"), max_length=20, choices=CABLE_SIDE_CHOICES, default="Left"
    )
    contracted_demand = models.CharField(_("Contracted Demand"), max_length=8)
    fire_exit = models.BooleanField(_("Transformer Fire Exit"), default=False)
    fire_transformer_power = models.FloatField(_("Fire Transformer Power"), null=True, blank=True)
    fire_transformer_demand = models.FloatField(_("Fire Transformer Demand"), null=True, blank=True)
    fire_transformer_impedance = models.FloatField(
        _("Fire Transformer Impedance"), null=True, blank=True
    )
    fire_transformer_type = models.CharField(
        _("Fire Transformer Type"), choices=TYPE_CHOICES, max_length=3, blank=True, null=True
    )
    measurements_consumers_quantity = models.PositiveIntegerField(_("Measurements/Consumers"))
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

    gimi_study = models.BooleanField(_("Gimi Study?"), blank=True, null=True)
    icc3f = models.FloatField(_("Icc3f"), blank=True, null=True)
    icc2f = models.FloatField(_("Icc2f"), blank=True, null=True)
    iccftmax = models.FloatField(_("Icc3f"), blank=True, null=True)
    iccftmin = models.FloatField(_("Icc3f"), blank=True, null=True)
    have_study = models.BooleanField(_("Have Study?"), blank=True, null=True)
    study_prediction = models.DateField(
        _("Study Prediction"), auto_now=False, auto_now_add=False, blank=True, null=True
    )
    breakers_quantity = models.PositiveIntegerField(_("Breakers Quantity"))


class Consumer(models.Model):
    checklist = models.ForeignKey(ChecklistC, on_delete=models.CASCADE, related_name="consumers")
    transformers_quantity = models.PositiveIntegerField(_("Transformers"))


class Transformer(models.Model):
    consumer = models.ForeignKey(
        Consumer, on_delete=models.CASCADE, related_name="transformers", null=True, blank=True
    )
    power = models.FloatField(_("Transformer Power"))
    impedance = models.FloatField(_("Impedance"), blank=True, null=True)
    demand = models.FloatField(_("Demand"), blank=True, null=True)
    type = models.CharField(_("Type"), choices=TYPE_CHOICES, max_length=3, blank=True, null=True)


class CurrentTransformer(models.Model):
    checklist = models.ForeignKey(
        ChecklistC, on_delete=models.CASCADE, related_name="current_transformers"
    )
    ratio = models.CharField(_("CT Ratio"), max_length=10)
    accuracy = models.CharField(_("CT Accuracy"), max_length=30)
