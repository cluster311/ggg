# Generated by Django 2.2.4 on 2019-11-09 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0005_consulta_centro_de_salud'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='carpeta_familiar',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='miembros', to='pacientes.CarpetaFamiliar'),
        ),
    ]
