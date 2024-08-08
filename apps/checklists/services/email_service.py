from django.conf import settings
from django.core.mail import send_mail


def send_new_checklist_email(instance):
    subject = f"Grupo Gimi - Novo Checklist para preenchimento ({instance.process_number})"
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
            .code {{
                background-color: #f0f0f0;
                padding: 2px 4px;
                border-radius: 4px;
                font-family: monospace;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <p>Olá <strong>{instance.client_name}</strong>!</p>
        <p>Um novo checklist do pedido {instance.process_number} do Grupo Gimi foi enviado. 🎉</p>
        <p>Insira o ID <span class="code">{instance.id}</span> em nosso webapp para prosseguir.</p>
        <a href="https://checklist-web-psi.vercel.app/checklist" target="_blank" class="btn">Acessar Webapp</a>
    </body>
    </html>
    """
    email_from = settings.EMAIL_HOST_USER
    recipient_list = instance.client_email.replace(" ", "").split(",")
    recipient_list.append(instance.user.email)

    send_mail(
        subject=subject,
        message=f"Cole o ID: {instance.id} em nosso webapp",
        from_email=email_from,
        recipient_list=recipient_list,
        html_message=message,
        fail_silently=False,
    )
