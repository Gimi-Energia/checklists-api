# Generated by Django 4.2.4 on 2024-07-17 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklistsB', '0003_alter_checklistb_contractor_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklistb',
            name='concessionaire',
            field=models.CharField(blank=True, choices=[('CPFL', 'CPFL'), ('EDP-SP', 'EDP-SP'), ('EDP-ES', 'EDP-ES'), ('ELEKTRO', 'ELEKTRO')], default='CEEE', max_length=20, null=True),
        ),
    ]
