# Generated by Django 4.2.3 on 2023-08-25 20:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Semilleros', '0015_inscripcionsemillero'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inscripcionsemillero',
            name='clave_e',
        ),
    ]