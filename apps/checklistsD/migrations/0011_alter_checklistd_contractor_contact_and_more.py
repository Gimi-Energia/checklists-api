# Generated by Django 4.2.4 on 2024-12-02 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklistsD', '0010_alter_checklistd_concessionaire'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklistd',
            name='contractor_contact',
            field=models.CharField(max_length=70, verbose_name='Contractor Contact'),
        ),
        migrations.AlterField(
            model_name='checklistd',
            name='contractor_name',
            field=models.CharField(max_length=70, verbose_name='Contractor Name'),
        ),
        migrations.AlterField(
            model_name='checklistd',
            name='owner_contact',
            field=models.CharField(max_length=70, verbose_name='Owner Contact'),
        ),
        migrations.AlterField(
            model_name='checklistd',
            name='owner_name',
            field=models.CharField(max_length=70, verbose_name='Owner Name'),
        ),
    ]
