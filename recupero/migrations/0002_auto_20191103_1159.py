# Generated by Django 2.2.4 on 2019-11-03 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recupero', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prestacion',
            name='nomenclador',
        ),
        migrations.AddField(
            model_name='tipoprestacion',
            name='arancel',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=11),
        ),
        migrations.AddField(
            model_name='tipoprestacion',
            name='codigo',
            field=models.CharField(blank=True, help_text='Código del servicio (de nomenclador si corresponde)', max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='tipoprestacion',
            name='descripcion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tipoprestacion',
            name='observaciones',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tipoprestacion',
            name='tipo',
            field=models.PositiveIntegerField(choices=[(0, 'Desconocido'), (100, 'Consulta'), (200, 'Práctica'), (300, 'Internación'), (400, 'Laboratorio')], default=100),
        ),
    ]
