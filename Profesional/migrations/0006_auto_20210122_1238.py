# Generated by Django 3.1.2 on 2021-01-22 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profesional', '0005_profesional_valoracion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profesional',
            name='valoracion',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
