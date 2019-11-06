# Generated by Django 2.2.4 on 2019-11-06 02:42

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('recupero', '0005_auto_20191104_0034'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentoanexo',
            name='created',
            field=model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created'),
        ),
        migrations.AddField(
            model_name='documentoanexo',
            name='modified',
            field=model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified'),
        ),
        migrations.AddField(
            model_name='factura',
            name='created',
            field=model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created'),
        ),
        migrations.AddField(
            model_name='factura',
            name='estado',
            field=models.PositiveIntegerField(choices=[(100, 'Nueva factura'), (300, 'Enviada'), (400, 'Rechazada'), (500, 'Aceptada'), (500, 'Pagada')], default=100),
        ),
        migrations.AddField(
            model_name='factura',
            name='modified',
            field=model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified'),
        ),
    ]
