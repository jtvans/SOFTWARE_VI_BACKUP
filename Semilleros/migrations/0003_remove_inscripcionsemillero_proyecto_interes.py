# Generated by Django 4.2.3 on 2023-08-31 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Semilleros', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inscripcionsemillero',
            name='proyecto_interes',
        ),
    ]