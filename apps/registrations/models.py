from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.checklists.models import COMPANIES, Checklist

MATERIAL_CHOICES = (
    ("Uso e consumo", "Uso e consumo"),
    ("Revenda", "Revenda"),
    ("Industrialização", "Industrialização"),
)


class Registration(models.Model):
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
    billing_cnpj = models.CharField(_("Billing CNPJ"), max_length=18)
    is_taxpayer = models.BooleanField(_("Is Taxpayer"), default=True)
    deadline = models.DateField(_("Deadline"), blank=True, null=True)
    minimum_value = models.FloatField(_("Minimum Value"), blank=True, null=True)
    material_destination = models.CharField(
        _("Material Destination"), max_length=50, choices=MATERIAL_CHOICES
    )
    nf_email = models.TextField(_("NF Emails"))
    additional_data = models.TextField(_("Additional Data"), blank=True, null=True)

    street = models.CharField(_("Street"), max_length=255)
    number = models.CharField(_("Number"), max_length=20)
    complement = models.CharField(_("Complement"), max_length=255, blank=True, null=True)
    neighborhood = models.CharField(_("Neighborhood"), max_length=100)
    city = models.CharField(_("City"), max_length=100)
    state = models.CharField(_("State"), max_length=50)
    zip_code = models.CharField(_("Zip Code"), max_length=20)
    access_restriction = models.CharField(
        _("Access Restriction"), max_length=100, blank=True, null=True
    )

    payment_condition = models.CharField(_("Payment Condition"), max_length=120)
    down_payment_date = models.DateField(_("Down Payment Date"), blank=True, null=True)

    tr_name = models.CharField(_("TR Name"), max_length=50)
    tr_phone = models.CharField(_("TR Phone"), max_length=15)
    tr_email = models.EmailField(_("TR Email"), max_length=254)
    tr_name_2 = models.CharField(_("TR Name"), max_length=50, blank=True, null=True)
    tr_phone_2 = models.CharField(_("TR Phone"), max_length=15, blank=True, null=True)
    tr_email_2 = models.EmailField(_("TR Email"), max_length=254, blank=True, null=True)

    mr_name = models.CharField(_("MR Name"), max_length=50)
    mr_phone = models.CharField(_("MR Phone"), max_length=15)
    mr_email = models.EmailField(_("MR Email"), max_length=254)
    mr_name_2 = models.CharField(_("MR Name"), max_length=50, blank=True, null=True)
    mr_phone_2 = models.CharField(_("MR Phone"), max_length=15, blank=True, null=True)
    mr_email_2 = models.EmailField(_("MR Email"), max_length=254, blank=True, null=True)

    fr_name = models.CharField(_("FR Name"), max_length=50)
    fr_phone = models.CharField(_("FR Phone"), max_length=15)
    fr_email = models.EmailField(_("FR Email"), max_length=254)
    fr_name_2 = models.CharField(_("FR Name"), max_length=50, blank=True, null=True)
    fr_phone_2 = models.CharField(_("FR Phone"), max_length=15, blank=True, null=True)
    fr_email_2 = models.EmailField(_("FR Email"), max_length=254, blank=True, null=True)

    lr_name = models.CharField(_(""), max_length=50, blank=True, null=True)
    lr_email = models.EmailField(_("LR Email"), max_length=254, blank=True, null=True)
    lr_phone = models.CharField(_("LR Phone"), max_length=15, blank=True, null=True)
    lr_document = models.CharField(_(""), max_length=14, blank=True, null=True)

    def __str__(self):
        return self.process_number
