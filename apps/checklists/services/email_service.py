from django.conf import settings
from django.core.mail import send_mail


def send_new_checklist_email(instance):
    url = f"https://checklist-web-psi.vercel.app/checklist/{instance.id}"
    title = f"{instance.company} - {instance.process_number}"
    subject = f"Grupo Gimi - Novo checklist para preenchimento ({title})"
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
        <p>Número Auxiliar: {instance.auxiliary_number}</p>
        <p>Nome da Obra: {instance.construction_name}</p>
        <p>ID: <span class="code">{instance.id}</span></p>
        <a href="{url}" target="_blank" class="btn">Acessar Checklist</a>
    </body>
    </html>
    """
    email_from = settings.EMAIL_HOST_USER
    recipient_list = instance.client_email.replace(" ", "").split(",")
    recipient_list.append(instance.user.email)

    send_mail(
        subject=subject,
        message=f"Novo checklist: {url}",
        from_email=email_from,
        recipient_list=recipient_list,
        html_message=message,
        fail_silently=False,
    )
