# Generated by Django 4.2.4 on 2024-11-07 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklistsA', '0012_alter_checklista_gimi_study_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklista',
            name='concessionaire',
            field=models.CharField(blank=True, choices=[('CEEE', 'CEEE'), ('CELESC', 'CELESC'), ('CEMIG', 'CEMIG'), ('CERIPA', 'CERIPA'), ('COELBA', 'COELBA'), ('CPFL', 'CPFL'), ('EDP-SP', 'EDP-SP'), ('EDP-ES', 'EDP-ES'), ('ELEKTRO', 'ELEKTRO'), ('ENEL', 'ENEL'), ('ENERGISA', 'ENERGISA'), ('EQUATORIAL', 'EQUATORIAL'), ('LIGHT', 'LIGHT')], max_length=20, null=True),
        ),
    ]