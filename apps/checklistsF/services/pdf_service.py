import tempfile

from django.utils.html import escape
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from apps.checklistsF.models import ChecklistF


def draw_header(c, image_path, width, height, margin):
    image_width = 1.6 * inch
    image_height = inch
    image_x = width - margin - image_width
    image_y = height - margin - image_height + 50
    c.drawImage(image_path, image_x, image_y, width=image_width, height=image_height)


def draw_footer(c, page_number, width):
    c.setFont("Helvetica", 8)
    footer_text = f"Página {page_number}"
    text_width = c.stringWidth(footer_text, "Helvetica", 8)
    c.drawString((width - text_width) / 2, 0.5 * inch, footer_text)


def add_page(c, width, height, page_number, margin, company):
    c.showPage()
    page_number += 1
    draw_header(c, f"setup/images/logo_{company}.png", width, height, margin)
    draw_footer(c, page_number, width)
    return page_number, height - margin - 1.3 * inch


def generate_pdf(instance):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        filename = tmpfile.name

    checklist = ChecklistF.objects.get(id=instance.id)
    substations = checklist.substations.all()
    current_transformers = checklist.current_transformers.all()

    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    margin = inch
    line_height = 14
    page_number = 1

    company = checklist.company.lower()
    draw_header(c, f"setup/images/logo_{company}.png", width, height, margin)
    draw_footer(c, page_number, width)

    current_height = height - margin - inch

    c.setFont("Helvetica", 14)
    title = "Checklist Subestações PMT"
    text_width = c.stringWidth(title, "Helvetica", 14)
    c.drawString((width - text_width) / 2, current_height, title)
    current_height -= line_height * 2

    c.line(margin, current_height, width - margin, current_height)
    current_height -= line_height * 2

    c.setFont("Helvetica", 10)

    study_prediction = (
        checklist.study_prediction.strftime("%d/%m/%Y")
        if checklist.study_prediction is not None
        else ""
    )

    main_details = [
        f"Número do processo: {escape(checklist.process_number)}",
        f"Quantidade de Subestações: {checklist.substations_quantity}",
        f"Proteção de Disjuntor: {'Sim' if checklist.breakers_protection else 'Não'}",
        f"Fornecimento do estudo: {'Gimi' if checklist.gimi_study else 'Cliente'}",
        f"Trifásico (Icc3f): {escape(checklist.icc3f)}",
        f"Bifásico (Icc2f): {escape(checklist.icc2f)}",
        f"Fase e Terra Máximo (IccfTmáx): {escape(checklist.iccftmax)}",
        f"Fase e Terra Mínimo (IccfTmín): {escape(checklist.iccftmin)}",
        f"Possui o estudo: {'Sim' if checklist.gimi_study else 'Não'}",
        f"Previsão do envio do estudo: {study_prediction}",
        f"Quantidade de Disjuntores: {checklist.breakers_quantity}",
    ]

    for detail in main_details:
        if current_height <= margin + (2 * line_height):
            page_number, current_height = add_page(c, width, height, page_number, margin, company)
        c.drawString(margin, current_height, detail)
        current_height -= line_height

    c.setFont("Helvetica", 14)
    substation_title = "Subestações"
    c.drawString(margin, current_height, substation_title)
    current_height -= line_height

    for substation in substations:
        substation_title = f"Subestação: {escape(substation.name)}"
        if current_height <= margin + (2 * line_height):
            page_number, current_height = add_page(c, width, height, page_number, margin, company)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin, current_height, substation_title)
        current_height -= line_height

        substation_details = [
            f" - Tensão Primária: {substation.primary_voltage} kV",
            f" - Uso do Painel: {substation.panel_usage}",
            f" - Lado de Entrada dos Cabos: {substation.cable_side}",
            f" - Quantidade de Transformadores: {substation.transformers_quantity}",
        ]

        c.setFont("Helvetica", 10)
        for detail in substation_details:
            if current_height <= margin + (2 * line_height):
                page_number, current_height = add_page(
                    c, width, height, page_number, margin, company
                )
            c.drawString(margin + 20, current_height, detail)
            current_height -= line_height

        for transformer in substation.transformers.all():
            transformer_details = f"- Potência: {transformer.power}"
            if current_height <= margin + (2 * line_height):
                page_number, current_height = add_page(
                    c, width, height, page_number, margin, company
                )
            c.drawString(margin + 20, current_height, transformer_details)
            current_height -= line_height

    c.setFont("Helvetica", 14)
    ct_title = "Definição dos TCs de Proteção"
    c.drawString(margin, current_height, ct_title)
    current_height -= line_height

    for ct in current_transformers:
        ct_details = f"Relação: {ct.ratio}, Exatidão: {ct.accuracy}"
        if current_height <= margin + (2 * line_height):
            page_number, current_height = add_page(c, width, height, page_number, margin, company)
        c.drawString(margin, current_height, ct_details)
        current_height -= line_height

    c.save()
    return filename
