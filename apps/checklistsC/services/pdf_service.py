import tempfile

from django.utils.html import escape
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from apps.checklistsC.models import ChecklistC


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

    checklist = ChecklistC.objects.get(id=instance.id)
    transformers = checklist.transformers.all()
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
    title = "Checklist Cabine Primária Convencional Multimedição"
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
        f"Concessionária: {escape(checklist.concessionaire)}",
        f"Outra Concessionária: {escape(checklist.other_concessionaire)}",
        f"Tensão Primária: {checklist.primary_voltage} kV",
        f"Uso do Painel: {checklist.panel_usage}",
        f"Lado da Entrada dos Cabos: {checklist.cable_side}",
        f"Demanda Contratada: {checklist.contracted_demand}",
        f"Saída Exclusiva para Transformador de Incêndio: {'Sim' if checklist.fire_exit else 'Não'}",
        f"Potência do Transformador de Incêndio: {checklist.fire_transformer_power}",
        f"Quantidade de Medições/Consumidores: {checklist.measurements_consumers_quantity}",
        f"Nome do Contratante: {escape(checklist.contractor_name)}",
        f"Documento do Contratante: {escape(checklist.contractor_document)}",
        f"Contato do Contratante: {escape(checklist.contractor_contact)}",
        f"Telefone do Contratante: {escape(checklist.contractor_phone)}",
        f"Rua do Contratante: {escape(checklist.contractor_street)}",
        f"Número do Contratante: {escape(checklist.contractor_number)}",
        f"Bairro do Contratante: {escape(checklist.contractor_neighborhood)}",
        f"Cidade do Contratante: {escape(checklist.contractor_city)}",
        f"Estado do Contratante: {escape(checklist.contractor_state)}",
        f"CEP do Contratante: {escape(checklist.contractor_zip_code)}",
        f"Nome do Proprietário: {escape(checklist.owner_name)}",
        f"Documento do Proprietário: {escape(checklist.owner_document)}",
        f"Contato do Proprietário: {escape(checklist.owner_contact)}",
        f"Telefone do Proprietário: {escape(checklist.owner_phone)}",
        f"Rua da Obra: {escape(checklist.contractor_street)}",
        f"Número da Obra: {escape(checklist.contractor_number)}",
        f"Bairro da Obra: {escape(checklist.contractor_neighborhood)}",
        f"Cidade da Obra: {escape(checklist.contractor_city)}",
        f"Estado da Obra: {escape(checklist.contractor_state)}",
        f"CEP da Obra: {escape(checklist.contractor_zip_code)}",
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
    transformer_title = "Medições/Consumidores"
    c.drawString(margin, current_height, transformer_title)
    current_height -= line_height

    for transformer in transformers:
        transformer_details = f"Potência: {transformer.power}"
        if current_height <= margin + (2 * line_height):
            page_number, current_height = add_page(c, width, height, page_number, margin, company)
        c.drawString(margin, current_height, transformer_details)
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