import tempfile

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from utils.pdf import generate_header


def generate_pdf(instance):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        filename = tmpfile.name

    document = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()

    header_table = generate_header(instance.company, styles)
    elements = [header_table, Spacer(1, 0.25 * inch)]

    elements.append(Spacer(1, 0.25 * inch))

    title = f"Checklist Serviços Opcionais ({instance.process_number})"
    title_para = Paragraph(title, styles["Title"])
    elements.append(title_para)
    elements.append(Spacer(1, 0.2 * inch))

    details_fat = [
        Paragraph(
            f"<b>Garantia Estendida:</b> {'Sim' if instance.extended_warranty else 'Não'}",
            styles["Normal"],
        ),
        Paragraph(
            f"<b>Estudo de Coordenação e Seletividade:</b> {'Sim' if instance.coord_selectivity else 'Não'}",
            styles["Normal"],
        ),
        Paragraph(
            f"<b>Serviço de Parametrização dos Relés de Proteção:</b> {'Sim' if instance.relay_parameterization else 'Não'}",
            styles["Normal"],
        ),
        Paragraph(
            f"<b>Comissionamento dos Relés de Proteção:</b> {'Sim' if instance.relay_commissioning else 'Não'}",
            styles["Normal"],
        ),
        Paragraph(
            f"<b>Comissionamento e Start-up dos Painéis:</b> {'Sim' if instance.panel_commissioning else 'Não'}",
            styles["Normal"],
        ),
        Paragraph(
            f"<b>Instalação de Barramento Blindado:</b> {'Sim' if instance.busbar_installation else 'Não'}",
            styles["Normal"],
        ),
        Paragraph(
            f"<b>Aquisição de Equipamentos de Proteção (EPI e EPC):</b> {'Sim' if instance.protection_equipment else 'Não'}",
            styles["Normal"],
        ),
    ]

    for detail in details_fat:
        elements.append(detail)
        elements.append(Spacer(1, 0.1 * inch))

    document.build(elements)

    return filename
