from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.checklists.models import COMPANIES, Checklist

PANEL_USAGE_CHOICES = [("Sheltered", "Sheltered"), ("Unsheltered", ("Unsheltered"))]

CABLE_SIDE_CHOICES = [("Left", "Left"), ("Right", "Right")]

TYPE_CHOICES = [("Air", "Air"), ("Oil", "Oil")]


class ChecklistF(models.Model):
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

    substations_quantity = models.PositiveIntegerField(_("Substations Quantity"))

    breakers_protection = models.BooleanField(_("Breakers Protection?"), default=True)
    gimi_study = models.BooleanField(_("Gimi Study?"), default=False)
    icc3f = models.FloatField(_("Icc3f"), blank=True, null=True)
    icc2f = models.FloatField(_("Icc2f"), blank=True, null=True)
    iccftmax = models.FloatField(_("Icc3f"), blank=True, null=True)
    iccftmin = models.FloatField(_("Icc3f"), blank=True, null=True)
    have_study = models.BooleanField(_("Have Study?"), default=False)
    study_prediction = models.DateField(
        _("Study Prediction"), auto_now=False, auto_now_add=False, blank=True, null=True
    )

    breakers_quantity = models.PositiveIntegerField(_("Breakers Quantity"))


class Substation(models.Model):
    checklist = models.ForeignKey(ChecklistF, on_delete=models.CASCADE, related_name="substations")
    name = models.CharField(_("Substation Name"), max_length=50)
    primary_voltage = models.FloatField(_("Primary Voltage (kV)"))
    panel_usage = models.CharField(
        _("Panel Usage"), max_length=20, choices=PANEL_USAGE_CHOICES, default="Sheltered"
    )
    cable_side = models.CharField(
        _("Cable Side"), max_length=20, choices=CABLE_SIDE_CHOICES, default="Left"
    )
    transformers_quantity = models.PositiveIntegerField(_("Transformers Quantity"))


class CurrentTransformer(models.Model):
    checklist = models.ForeignKey(
        ChecklistF, on_delete=models.CASCADE, related_name="current_transformers"
    )
    ratio = models.CharField(_("CT Ratio"), max_length=10)
    accuracy = models.CharField(_("CT Accuracy"), max_length=30)


class Transformer(models.Model):
    substation = models.ForeignKey(
        Substation, on_delete=models.CASCADE, related_name="transformers"
    )
    power = models.FloatField(_("Transformer Power"))
    impedance = models.FloatField(_("Impedance"), blank=True, null=True)
    demand = models.FloatField(_("Demand"), blank=True, null=True)
    type = models.CharField(_("Type"), choices=TYPE_CHOICES, max_length=3, blank=True, null=True)
