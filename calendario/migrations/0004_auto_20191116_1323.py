# Generated by Django 2.2.4 on 2019-11-16 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendario', '0003_auto_20191112_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='estado',
            field=models.IntegerField(choices=[(0, 'Disponible'), (1, 'Asignado'), (2, 'Esperando en sala'), (3, 'Atendido'), (4, 'Cancelado por el paciente'), (5, 'Cancelado por el establecimiento')], default=0),
        ),
    ]
