import json

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Send an email with a password and link to the app"  # python manage.py sendpasswords

    def handle(self, *args, **kwargs):
        with open("apps/users/fixtures/users_data.json", "r") as f:
            users = json.load(f)

        for user in users:
            email = user["fields"]["email"]
            password = user["fields"]["password"]
            message = f"""
            Olá, sua senha é: {password}, use seu e-mail para realizar o login.
            Acesse o app em https://checklist-web-psi.vercel.app/login
            """
            send_mail(
                "Acesso ao App Checklist Web",
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f"Email successfully sent to {email}"))
