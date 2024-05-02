from django.conf import settings
from django.core.mail import EmailMessage

from apps.checklistsB.services.pdf_service import generate_pdf
from apps.users.models import User


def send_registration_email(instance):
    subject = (
        f"Checklist Cabine Primária Simplificada Medição MT (Enel) - {instance.process_number}"
    )
    users = User.objects.all()
    recipient_list = [user.email for user in users]
    email_from = settings.EMAIL_HOST_USER

    email = EmailMessage(
        subject=subject,
        body=f"Checklist cabine primária simplificada medição MT - Enel ({instance.process_number}) foi respondido.",
        from_email=email_from,
        to=recipient_list,
    )

    pdf_file = generate_pdf(instance)
    with open(pdf_file, "rb") as pdf_file:
        email.attach(
            f"Checklist_Cabine_Primaria_Simplificada_Medicao_MT_Enel_{instance.process_number}.pdf",
            pdf_file.read(),
            "application/pdf",
        )

    email.send()