# Generated by Django 2.2.10 on 2020-06-12 11:55

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cie10_django', '0001_initial'),
        ('centros_de_salud', '0011_auto_20191117_1800'),
        ('pacientes', '0014_auto_20200426_1155'),
        ('recupero', '0012_auto_20200524_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='centro_de_salud',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='facturas_centro', to='centros_de_salud.CentroDeSalud'),
        ),
        migrations.AddField(
            model_name='factura',
            name='codigo_cie_principal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='diagnositicos_principales_factura', to='cie10_django.CIE10'),
        ),
        migrations.AddField(
            model_name='factura',
            name='codigos_cie_secundarios',
            field=models.ManyToManyField(blank=True, null=True, related_name='diagnositicos_secundarios_factura', to='cie10_django.CIE10'),
        ),
        migrations.AddField(
            model_name='factura',
            name='fecha_atencion',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='factura',
            name='paciente',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='paciente_factura', to='pacientes.Paciente'),
        ),
        migrations.CreateModel(
            name='FacturaPrestacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('consulta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prestacionesFactura', to='pacientes.Consulta')),
                ('tipo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='recupero.TipoPrestacion')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
