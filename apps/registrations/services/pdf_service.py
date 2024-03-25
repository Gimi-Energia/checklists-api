import tempfile

from django.utils.html import escape
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from apps.registrations.models import MATERIAL_CHOICES


def generate_pdf(registration):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        filename = tmpfile.name

    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica", 14)
    line_height = 14
    margin = inch
    current_height = height - margin

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
        c.drawString(inch, current_height, detail)
        current_height -= line_height

    c.save()
    return filename
