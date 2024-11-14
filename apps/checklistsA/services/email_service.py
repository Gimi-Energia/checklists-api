from django.conf import settings
from django.core.mail import EmailMessage

from apps.checklistsA.services.pdf_service import generate_pdf
from apps.users.models import User


def send_checklist_email(instance, transformers_data, current_transformers_data):
    title = f"{instance.company} {instance.process_number}-{instance.item}"
    subject = f"Checklist Cabine Primária Convencional - {title}"
    users = User.objects.all()
    recipient_list = [user.email for user in users]
    recipient_list += instance.parent_checklist.client_email.replace(" ", "").split(",")
    email_from = settings.EMAIL_HOST_USER

    email = EmailMessage(
        subject=subject,
        body=f"Checklist cabine primária convencional ({title}) foi respondido.",
        from_email=email_from,
        to=recipient_list,
    )

    pdf_file = generate_pdf(instance, transformers_data, current_transformers_data)
    with open(pdf_file, "rb") as pdf_file:
        email.attach(f"Checklist A {title}.pdf", pdf_file.read(), "application/pdf")

    email.send()
