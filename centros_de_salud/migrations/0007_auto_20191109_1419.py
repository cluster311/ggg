# Generated by Django 2.2.4 on 2019-11-09 17:19

import address.models
from django.db import migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('centros_de_salud', '0006_auto_20191028_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='centrodesalud',
            name='direccion',
            field=address.models.AddressField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='address.Address'),
        ),
    ]
