# Generated by Django 2.2.13 on 2020-09-08 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0017_consulta_obra_social'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresapaciente',
            name='ultimo_recibo_de_sueldo',
            field=models.DateField(blank=True, null=True),
        ),
    ]
