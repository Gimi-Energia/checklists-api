from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import escape

from apps.registrations.models import MATERIAL_CHOICES
from apps.users.models import User


def send_registration_email(registration):
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

    details_html = "<li>" + "</li><li>".join(details) + "</li>"

    subject = "Confirmação de Dados Cadastrais"
    message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                font-size: 16px;
            }}
            .btn {{
                display: inline-block;
                background-color: #f0f0f0;
                padding: 8px 16px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                border-radius: 10px;
                margin-top: 10px;
                border: 2px solid black;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <p>Um novo checklist de dados cadastrais foi respondido com sucesso. Veja os detalhes abaixo:</p>
        <ul>{details_html}</ul>
        <p>Para mais detalhes, acesse nosso webapp.</p>
        <a href="https://checklist-web-psi.vercel.app/login" target="_blank" class="btn">Acessar Webapp</a>
    </body>
    </html>
    """

    users = User.objects.all()
    recipient_list = [user.email for user in users]
    email_from = settings.EMAIL_HOST_USER

    send_mail(
        subject=subject,
        message=f"Checklist de dados cadastrais do CF {registration.process_number} foi respondido.",
        from_email=email_from,
        recipient_list=recipient_list,
        html_message=message,
        fail_silently=False,
    )
