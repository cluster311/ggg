# Generated by Django 2.2.4 on 2019-11-12 21:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendario', '0002_auto_20191008_1448'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='turno',
            options={'permissions': [('can_schedule_turno', 'Puede agendar un turno')]},
        ),
    ]
