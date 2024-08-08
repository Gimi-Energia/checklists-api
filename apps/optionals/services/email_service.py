from django.conf import settings
from django.core.mail import EmailMessage

from apps.optionals.services.pdf_service import generate_pdf
from apps.users.models import User


def send_optionals_email(instance):
    subject = f"Checklist Serviços Opcionais {instance.process_number}"
    users = User.objects.all()
    recipient_list = [user.email for user in users]
    recipient_list += instance.parent_checklist.client_email.replace(" ", "").split(",")
    email_from = settings.EMAIL_HOST_USER

    email = EmailMessage(
        subject=subject,
        body=f"Checklist de serviços opcionais ({instance.process_number}) foi respondido.",
        from_email=email_from,
        to=recipient_list,
    )

    pdf_file = generate_pdf(instance)
    with open(pdf_file, "rb") as pdf_file:
        email.attach(
            f"Checklist_Servicos_Opcionais_{instance.process_number}.pdf",
            pdf_file.read(),
            "application/pdf",
        )

    email.send()
