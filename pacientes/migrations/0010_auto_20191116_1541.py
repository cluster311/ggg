# Generated by Django 2.2.4 on 2019-11-16 18:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0009_paciente_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='consulta',
            old_name='diagnostico',
            new_name='evolucion',
        ),
    ]
