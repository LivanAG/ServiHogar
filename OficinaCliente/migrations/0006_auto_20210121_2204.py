# Generated by Django 3.1.2 on 2021-01-21 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OficinaCliente', '0005_auto_20210112_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='orden',
            name='valoracion_Cliente',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='orden',
            name='valoracion_Profesional',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]