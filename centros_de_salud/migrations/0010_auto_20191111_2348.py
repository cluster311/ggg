# Generated by Django 2.2.4 on 2019-11-12 02:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('centros_de_salud', '0009_especialidad_tiempo_predeterminado_turno'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='centrodesalud',
            options={'permissions': [('can_view_tablero', 'Ver tableros de comandos')], 'verbose_name': 'Centro de Salud', 'verbose_name_plural': 'Centros de Salud'},
        ),
    ]