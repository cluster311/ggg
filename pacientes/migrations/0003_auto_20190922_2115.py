# Generated by Django 2.2.4 on 2019-09-22 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0002_telefono'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='apellido',
            field=models.CharField(max_length=30),
        ),
    ]
