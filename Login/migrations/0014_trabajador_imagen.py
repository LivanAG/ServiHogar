# Generated by Django 3.1.2 on 2021-01-26 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0013_trabajador'),
    ]

    operations = [
        migrations.AddField(
            model_name='trabajador',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='Imagenes de Perfil de Trabajadores'),
        ),
    ]
