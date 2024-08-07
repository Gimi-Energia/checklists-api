# Generated by Django 4.2.4 on 2024-05-03 18:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('checklists', '0006_checklist_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChecklistF',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('process_number', models.CharField(max_length=10, verbose_name='Process Number')),
                ('company', models.CharField(choices=[('Gimi', 'Gimi'), ('GBL', 'GBL'), ('GPB', 'GPB'), ('GS', 'GS'), ('GIR', 'GIR')], default='Gimi', max_length=4, verbose_name='Company')),
                ('substations_quantity', models.PositiveIntegerField(verbose_name='Substations Quantity')),
                ('breakers_protection', models.BooleanField(default=True, verbose_name='Breakers Protection?')),
                ('gimi_study', models.BooleanField(default=False, verbose_name='Gimi Study?')),
                ('icc3f', models.FloatField(blank=True, null=True, verbose_name='Icc3f')),
                ('icc2f', models.FloatField(blank=True, null=True, verbose_name='Icc2f')),
                ('iccftmax', models.FloatField(blank=True, null=True, verbose_name='Icc3f')),
                ('iccftmin', models.FloatField(blank=True, null=True, verbose_name='Icc3f')),
                ('have_study', models.BooleanField(default=False, verbose_name='Have Study?')),
                ('study_prediction', models.DateField(blank=True, null=True, verbose_name='Study Prediction')),
                ('breakers_quantity', models.PositiveIntegerField(verbose_name='Breakers Quantity')),
                ('parent_checklist', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='checklists.checklist', verbose_name='Parent Checklist')),
            ],
        ),
        migrations.CreateModel(
            name='Substation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Substation Name')),
                ('primary_voltage', models.FloatField(verbose_name='Primary Voltage (kV)')),
                ('panel_usage', models.CharField(choices=[('Sheltered', 'Sheltered'), ('Unsheltered', 'Unsheltered')], default='Sheltered', max_length=20, verbose_name='Panel Usage')),
                ('cable_side', models.CharField(choices=[('Left', 'Left'), ('Right', 'Right')], default='Left', max_length=20, verbose_name='Cable Side')),
                ('transformers_quantity', models.PositiveIntegerField(verbose_name='Transformers Quantity')),
                ('checklist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='substations', to='checklistsF.checklistf')),
            ],
        ),
        migrations.CreateModel(
            name='Transformer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('power', models.PositiveIntegerField(verbose_name='Transformer Power')),
                ('substation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='substations', to='checklistsF.substation')),
            ],
        ),
        migrations.CreateModel(
            name='CurrentTransformer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ratio', models.CharField(max_length=10, verbose_name='CT Ratio')),
                ('accuracy', models.CharField(max_length=30, verbose_name='CT Accuracy')),
                ('checklist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='current_transformers', to='checklistsF.checklistf')),
            ],
        ),
    ]
