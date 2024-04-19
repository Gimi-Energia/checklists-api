# Generated by Django 4.2.4 on 2024-04-03 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0007_alter_registration_minimum_value'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registration',
            name='budget_satisfaction',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='commercial_satisfaction',
        ),
        migrations.AddField(
            model_name='registration',
            name='company',
            field=models.CharField(choices=[('Gimi', 'Gimi'), ('GBL', 'GBL'), ('GPB', 'GPB'), ('GS', 'GS'), ('GIR', 'GIR')], default='Gimi', max_length=4, verbose_name='Company'),
        ),
    ]