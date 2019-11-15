# Generated by Django 2.2.4 on 2019-11-15 02:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('centros_de_salud', '0010_auto_20191111_2348'),
        ('pacientes', '0007_auto_20191114_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='consulta',
            name='especialidad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='consultas', to='centros_de_salud.Especialidad'),
        ),
    ]