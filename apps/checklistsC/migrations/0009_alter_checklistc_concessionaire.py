# Generated by Django 4.2.4 on 2024-07-17 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklistsC', '0008_alter_checklistc_contractor_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklistc',
            name='concessionaire',
            field=models.CharField(blank=True, choices=[('CEEE', 'CEEE'), ('CELESC', 'CELESC'), ('CEMIG', 'CEMIG'), ('CERIPA', 'CERIPA'), ('COELBA', 'COELBA'), ('CPFL', 'CPFL'), ('EDP-SP', 'EDP-SP'), ('EDP-ES', 'EDP-ES'), ('ELEKTRO', 'ELEKTRO'), ('ENEL', 'ENEL'), ('ENERGISA', 'ENERGISA'), ('EQUATORIAL', 'EQUATORIAL'), ('LIGHT', 'LIGHT')], default='CEEE', max_length=20, null=True),
        ),
    ]
