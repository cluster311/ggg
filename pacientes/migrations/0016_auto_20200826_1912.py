# Generated by Django 2.2.13 on 2020-08-26 22:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0015_paciente_ultima_actualizacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='ultima_actualizacion',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
