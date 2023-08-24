# Generated by Django 4.2.3 on 2023-08-23 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Semilleros', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='semillero',
            name='nombre_semillero',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='semillero',
            name='nivel_ingles_entiende',
            field=models.CharField(choices=[('bajo', 'Bajo'), ('medio', 'Medio'), ('alto', 'Alto')], max_length=300),
        ),
        migrations.AlterField(
            model_name='semillero',
            name='nivel_ingles_escribe',
            field=models.CharField(choices=[('bajo', 'Bajo'), ('medio', 'Medio'), ('alto', 'Alto')], max_length=300),
        ),
        migrations.AlterField(
            model_name='semillero',
            name='nivel_ingles_habla',
            field=models.CharField(choices=[('bajo', 'Bajo'), ('medio', 'Medio'), ('alto', 'Alto')], max_length=300),
        ),
        migrations.AlterField(
            model_name='semillero',
            name='nivel_ingles_lee',
            field=models.CharField(choices=[('bajo', 'Bajo'), ('medio', 'Medio'), ('alto', 'Alto')], max_length=300),
        ),
    ]