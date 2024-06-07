# Generated by Django 4.2.4 on 2024-05-05 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklistsC', '0004_alter_checklistc_cable_side'),
    ]

    operations = [
        migrations.AddField(
            model_name='transformer',
            name='demand',
            field=models.FloatField(blank=True, null=True, verbose_name='Demand'),
        ),
        migrations.AddField(
            model_name='transformer',
            name='impedance',
            field=models.FloatField(blank=True, null=True, verbose_name='Impedance'),
        ),
        migrations.AddField(
            model_name='transformer',
            name='type',
            field=models.CharField(blank=True, choices=[('Air', 'Air'), ('Oil', 'Oil')], max_length=3, null=True, verbose_name='Type'),
        ),
    ]