# Generated by Django 2.2.4 on 2019-11-16 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendario', '0007_merge_20191116_1353'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='turno',
            options={'permissions': [('can_schedule_turno', 'Puede agendar un turno'), ('can_view_misturnos', 'Puede ver Mis Turnos'), ('can_cancel_turno', 'Puede cancelar sus turnos'), ('can_gestionar_turnos', 'Puede gestionar turnos')]},
        ),
    ]