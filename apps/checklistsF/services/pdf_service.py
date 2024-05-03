import tempfile

from django.utils.html import escape
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from apps.checklistsF.models import ChecklistF


def generate_pdf(instance):
    pass
