# Generated by Django 2.2.4 on 2019-11-17 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('especialidades', '0002_auto_20191116_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medidaanexaenconsulta',
            name='valor',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=13),
        ),
    ]
