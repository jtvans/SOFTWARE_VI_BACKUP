# Generated by Django 4.2.3 on 2023-08-30 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Semilleros', '0039_actividadessemillero_adjunto_actividad_e'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inscripcionsemillero',
            name='proyectos',
        ),
        migrations.RemoveField(
            model_name='semillero',
            name='proyectos',
        ),
    ]
