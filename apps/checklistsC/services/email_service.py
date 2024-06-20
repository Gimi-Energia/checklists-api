from django.conf import settings
from django.core.mail import EmailMessage

from apps.checklistsC.services.pdf_service import generate_pdf
from apps.users.models import User


def send_checklist_email(instance):
    subject = f"Checklist Cabine Primária Convencional Multimedição - {instance.process_number}-{instance.item}"
    users = User.objects.all()
    recipient_list = [user.email for user in users]
    email_from = settings.EMAIL_HOST_USER

    email = EmailMessage(
        subject=subject,
        body=f"Checklist cabine primária convencional multimedição ({instance.process_number}-{instance.item}) foi respondido.",
        from_email=email_from,
        to=recipient_list,
    )

    pdf_file = generate_pdf(instance)
    with open(pdf_file, "rb") as pdf_file:
        email.attach(
            f"Checklist_Cabine_Primaria_Convencional_Multimedicao_{instance.process_number}-{instance.item}.pdf",
            pdf_file.read(),
            "application/pdf",
        )

    email.send()
