# Generated by Django 2.2.4 on 2019-11-12 02:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profesionales', '0007_auto_20191109_1054'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profesional',
            options={'permissions': [('can_view_tablero', 'Ver tableros de comandos')], 'verbose_name_plural': 'Profesionales'},
        ),
    ]
