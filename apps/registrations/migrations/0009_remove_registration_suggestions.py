# Generated by Django 4.2.4 on 2024-04-19 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0008_remove_registration_budget_satisfaction_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registration',
            name='suggestions',
        ),
    ]