from django.conf import settings
from django.core.mail import send_mail


def send_new_checklist_email(checklist):
    subject = "Grupo Gimi - Novo Checklist Criado"
    message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            /* Seu CSS aqui */
        </style>
    </head>
    <body>
        <p>Olá <strong>{checklist.client_name}</strong>!</p>
        <p>Um novo checklist do Grupo Gimi foi enviado. 🎉</p>
        <p>Insira o ID <span class="code">{checklist.id}</span> em nosso webapp para prosseguir.</p>
        <a href="https://www.google.com/" target="_blank" class="btn">Acessar Webapp</a>
    </body>
    </html>
    """
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [checklist.client_email]

    send_mail(
        subject=subject,
        message=f"Cole o ID: {checklist.id} em nosso webapp",
        from_email=email_from,
        recipient_list=recipient_list,
        html_message=message,
        fail_silently=False,
    )
