# Generated by Django 2.2.4 on 2019-11-16 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendario', '0004_auto_20191116_1043'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='turno',
            options={'permissions': [('can_schedule_turno', 'Puede agendar un turno'), ('can_view_misturnos', 'Puede ver Mis Turnos')]},
        ),
    ]
