# Generated by Django 4.2.4 on 2024-05-03 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklistsE', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkliste',
            name='cable_side',
            field=models.CharField(choices=[('Left', 'Left'), ('Right', 'Right')], default='Left', max_length=20, verbose_name='Cable Side'),
        ),
    ]
