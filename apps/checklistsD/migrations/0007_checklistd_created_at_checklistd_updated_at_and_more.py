# Generated by Django 4.2.4 on 2024-08-08 15:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('checklistsD', '0006_remove_transformer_demand_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='checklistd',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Creation Date'),
        ),
        migrations.AddField(
            model_name='checklistd',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Update Date'),
        ),
        migrations.AlterField(
            model_name='checklistd',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
