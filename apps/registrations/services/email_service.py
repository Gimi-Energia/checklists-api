from django.conf import settings
from django.core.mail import EmailMessage

from apps.registrations.services.pdf_service import generate_pdf
from apps.users.models import User


def send_registration_email(registration):
    subject = f"Checklist Dados Cadastrais {registration.process_number}"
    users = User.objects.all()
    recipient_list = [user.email for user in users]
    email_from = settings.EMAIL_HOST_USER

    email = EmailMessage(
        subject=subject,
        body=f"Checklist de dados cadastrais ({registration.process_number}) foi respondido.",
        from_email=email_from,
        to=recipient_list,
    )

    pdf_file = generate_pdf(registration)
    with open(pdf_file, "rb") as pdf_file:
        email.attach(
            f"Checklist_Dados_Cadastrais_{registration.process_number}.pdf",
            pdf_file.read(),
            "application/pdf",
        )

    email.send()
