# Generated by Django 4.2.4 on 2024-03-20 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0003_alter_registration_additional_data_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='budget_satisfaction',
            field=models.PositiveIntegerField(verbose_name='Budget Satisfaction'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='commercial_satisfaction',
            field=models.PositiveIntegerField(verbose_name='Commercial Satisfaction'),
        ),
    ]
