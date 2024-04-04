import tempfile

from django.utils.html import escape
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from apps.registrations.models import MATERIAL_CHOICES


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
    draw_header(c, f"apps/registrations/images/logo_{company}.png", width, height, margin)
    draw_footer(c, page_number, width)
    return page_number, height - margin - 1.3 * inch


def generate_pdf(registration):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        filename = tmpfile.name

    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    margin = inch
    line_height = 14
    page_number = 1

    company = registration.company.lower()
    draw_header(c, f"apps/registrations/images/logo_{company}.png", width, height, margin)
    draw_footer(c, page_number, width)

    current_height = height - margin - inch

    c.setFont("Helvetica", 14)
    title = "Checklist Dados Cadastrais"
    text_width = c.stringWidth(title, "Helvetica", 14)
    c.drawString((width - text_width) / 2, current_height, title)
    current_height -= line_height * 2

    c.line(margin, current_height, width - margin, current_height)
    current_height -= line_height * 2

    c.setFont("Helvetica", 10)

    details = [
        f"Número do processo: {escape(registration.process_number)}",
        f"CNPJ de faturamento: {escape(registration.billing_cnpj)}",
        f"Contribuinte de ICMS: {'Sim' if registration.is_taxpayer else 'Não'}",
        f"Destino do material: {dict(MATERIAL_CHOICES).get(registration.material_destination, '')}",
        f"Emails NF: {escape(registration.nf_email)}",
        f"Rua: {escape(registration.street)}",
        f"Número: {escape(registration.number)}",
        f"Bairro: {escape(registration.neighborhood)}",
        f"Cidade: {escape(registration.city)}",
        f"Estado: {escape(registration.state)}",
        f"CEP: {escape(registration.zip_code)}",
        f"Condição de Pagamento: {escape(registration.payment_condition)}",
        f"Nome do responsável tecnico: {escape(registration.tr_name)}",
        f"Telefone do responsável tecnico: {escape(registration.tr_phone)}",
        f"Email do responsável tecnico: {escape(registration.tr_email)}",
        f"Nome do responsável pelo material: {escape(registration.mr_name)}",
        f"Telefone do responsável pelo material: {escape(registration.mr_phone)}",
        f"Email do responsável pelo material: {escape(registration.mr_email)}",
        f"Nome do responsável financeiro: {escape(registration.fr_name)}",
        f"Telefone do responsável financeiro: {escape(registration.fr_phone)}",
        f"Email do responsável financeiro: {escape(registration.fr_email)}",
        f"Satisfação comercial: {registration.commercial_satisfaction}",
        f"Satisfação orçamento: {registration.budget_satisfaction}",
    ]

    optional_fields = {
        "Data limite NF": registration.deadline,
        "Valor mínimo de faturamento": registration.minimum_value,
        "Dados adicionais OBS NF": registration.additional_data,
        "Complemento": registration.complement,
        "Restrição de acesso": registration.access_restriction,
        "Data sinal": registration.down_payment_date,
        "Sugestões": registration.suggestions,
        "Nome do responsável tecnico 2": registration.tr_name_2,
        "Telefone do responsável tecnico 2": registration.tr_phone_2,
        "Email do responsável tecnico 2": registration.tr_email_2,
        "Nome do responsável pelo material 2": registration.mr_name_2,
        "Telefone do responsável pelo material 2": registration.mr_phone_2,
        "Email do responsável pelo material 2": registration.mr_email_2,
        "Nome do responsável financeiro 2": registration.fr_name_2,
        "Telefone do responsável financeiro 2": registration.fr_phone_2,
        "Email do responsável financeiro 2": registration.fr_email_2,
    }

    for label, value in optional_fields.items():
        if value:
            details.append(f"{label}: {escape(str(value))}")

    for detail in details:
        if current_height <= margin + (2 * line_height):
            page_number, current_height = add_page(c, width, height, page_number, margin, company)
        c.drawString(margin, current_height, detail)
        current_height -= line_height

    c.save()
    return filename
