# Generated by Django 4.2.4 on 2024-08-08 15:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('checklistsE', '0005_alter_checkliste_contractor_phone_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkliste',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Creation Date'),
        ),
        migrations.AddField(
            model_name='checkliste',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Update Date'),
        ),
        migrations.AlterField(
            model_name='checkliste',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
