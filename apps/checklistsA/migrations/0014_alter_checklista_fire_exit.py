# Generated by Django 4.2.4 on 2024-11-07 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklistsA', '0013_alter_checklista_concessionaire'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklista',
            name='fire_exit',
            field=models.BooleanField(default=False, verbose_name='Transformer Fire Exit'),
        ),
    ]
