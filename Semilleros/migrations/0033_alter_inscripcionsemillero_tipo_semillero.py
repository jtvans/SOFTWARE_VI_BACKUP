# Generated by Django 4.2.3 on 2023-08-28 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Semilleros', '0032_alter_inscripcionsemillero_horas_semanales_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inscripcionsemillero',
            name='tipo_semillero',
            field=models.CharField(choices=[('unica', 'Fase Unica')], max_length=20),
        ),
    ]
