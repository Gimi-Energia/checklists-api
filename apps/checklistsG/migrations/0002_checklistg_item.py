# Generated by Django 4.2.4 on 2024-06-10 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklistsG', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='checklistg',
            name='item',
            field=models.CharField(default='1', max_length=3, verbose_name='Item'),
        ),
    ]
