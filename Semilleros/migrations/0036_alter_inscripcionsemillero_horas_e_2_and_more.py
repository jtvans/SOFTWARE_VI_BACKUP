# Generated by Django 4.2.3 on 2023-08-29 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Semilleros', '0035_inscripcionsemillero_direccion_e_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inscripcionsemillero',
            name='horas_e_2',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='inscripcionsemillero',
            name='institucion_e_2',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
