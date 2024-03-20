# Generated by Django 4.2.4 on 2024-03-19 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklists', '0002_alter_checklistproduct_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checklistproduct',
            name='status',
        ),
        migrations.AddField(
            model_name='checklistproduct',
            name='items_answered',
            field=models.JSONField(default=list, verbose_name='Item Answered'),
        ),
        migrations.AddField(
            model_name='checklistproduct',
            name='items_numbers',
            field=models.JSONField(default=list, verbose_name='Item Numbers'),
        ),
        migrations.AddField(
            model_name='checklistproduct',
            name='quantity',
            field=models.PositiveIntegerField(default=0, verbose_name='Quantity'),
            preserve_default=False,
        ),
    ]