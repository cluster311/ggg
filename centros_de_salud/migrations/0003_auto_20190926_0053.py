# Generated by Django 2.2.4 on 2019-09-26 00:53

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('centros_de_salud', '0002_auto_20190926_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='centrodesalud',
            name='descripcion',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
    ]