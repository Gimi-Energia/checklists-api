# Generated by Django 4.2.4 on 2024-08-08 15:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('checklists', '0012_remove_checklist_answered_art_checklist_art_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checklist',
            name='answered_optional',
        ),
        migrations.RemoveField(
            model_name='checklist',
            name='answered_registration',
        ),
        migrations.RemoveField(
            model_name='checklist',
            name='budget_number',
        ),
        migrations.AddField(
            model_name='checklist',
            name='optional_status',
            field=models.IntegerField(choices=[(1, 'PREVIOUSLY SENT'), (2, 'SENT'), (3, 'ANSWERED')], default=2, verbose_name='Answered Optional'),
        ),
        migrations.AddField(
            model_name='checklist',
            name='process_number',
            field=models.CharField(default=0, max_length=10, verbose_name='Process Number'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='checklist',
            name='registration_status',
            field=models.IntegerField(choices=[(1, 'PREVIOUSLY SENT'), (2, 'SENT'), (3, 'ANSWERED')], default=2, verbose_name='Answered Registration'),
        ),
        migrations.AddField(
            model_name='checklist',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Update Date'),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='art_status',
            field=models.IntegerField(choices=[(1, 'NOT SENT'), (2, 'SENT'), (3, 'ANSWERED')], default=1, verbose_name='ART Status'),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='client_email',
            field=models.TextField(verbose_name='Client Email'),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Creation Date'),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='products',
            field=models.ManyToManyField(through='checklists.ChecklistProduct', to='checklists.product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.CharField(max_length=1, primary_key=True, serialize=False, unique=True),
        ),
    ]
