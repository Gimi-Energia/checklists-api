# Generated by Django 4.2.4 on 2024-03-18 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklists', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklistproduct',
            name='status',
            field=models.CharField(choices=[('Opened', 'Opened'), ('Canceled', 'Canceled'), ('Answered', 'Answered')], default='Opened', max_length=8),
        ),
    ]
