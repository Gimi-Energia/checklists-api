# Generated by Django 4.2.4 on 2024-11-07 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklistsB', '0007_checklistb_contractor_latitude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklistb',
            name='concessionaire',
            field=models.CharField(blank=True, choices=[('CPFL', 'CPFL'), ('EDP-SP', 'EDP-SP'), ('EDP-ES', 'EDP-ES'), ('ELEKTRO', 'ELEKTRO')], max_length=20, null=True),
        ),
    ]
