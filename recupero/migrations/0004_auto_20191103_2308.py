# Generated by Django 2.2.4 on 2019-11-04 02:08

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0004_auto_20191103_2308'),
        ('recupero', '0003_tipoprestacion_anio_update'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prestacion',
            name='documentos_adjuntados',
        ),
        migrations.RemoveField(
            model_name='prestacion',
            name='factura',
        ),
        migrations.RemoveField(
            model_name='prestacion',
            name='fecha',
        ),
        migrations.AddField(
            model_name='documentoanexo',
            name='prestacion',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='documentos', to='recupero.Prestacion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='prestacion',
            name='consulta',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='prestaciones', to='pacientes.Consulta'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='prestacion',
            name='created',
            field=model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created'),
        ),
        migrations.AddField(
            model_name='prestacion',
            name='modified',
            field=model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified'),
        ),
        migrations.AddField(
            model_name='prestacion',
            name='observaciones',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='prestacion',
            name='cantidad',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='prestacion',
            name='tipo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='recupero.TipoPrestacion'),
        ),
    ]
