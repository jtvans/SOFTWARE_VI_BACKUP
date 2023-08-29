# Generated by Django 4.2.3 on 2023-08-28 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Semilleros', '0033_alter_inscripcionsemillero_tipo_semillero'),
    ]

    operations = [
        migrations.AddField(
            model_name='semillero',
            name='direccion',
            field=models.CharField(default=1, max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='semillero',
            name='fecha_nacimiento',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='semillero',
            name='lugar_expedicion',
            field=models.CharField(default=1, max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='semillero',
            name='lugar_nacimiento',
            field=models.CharField(default=1, max_length=40),
            preserve_default=False,
        ),
    ]
