# Generated by Django 3.1.6 on 2021-02-07 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0014_trabajador_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='resegna',
            field=models.CharField(blank=True, default=None, max_length=250, null=True),
        ),
    ]