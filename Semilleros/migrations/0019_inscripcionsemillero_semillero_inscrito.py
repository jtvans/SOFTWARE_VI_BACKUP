# Generated by Django 4.2.3 on 2023-08-28 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Semilleros', '0018_inscripcionsemillero_tipo_solicitante'),
    ]

    operations = [
        migrations.AddField(
            model_name='inscripcionsemillero',
            name='semillero_inscrito',
            field=models.EmailField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]