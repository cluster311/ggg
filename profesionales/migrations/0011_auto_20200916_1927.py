# Generated by Django 2.2.13 on 2020-09-16 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profesionales', '0010_auto_20191117_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profesional',
            name='tipo_documento',
            field=models.CharField(choices=[('DNI', 'DNI'), ('LC', 'LC'), ('LE', 'LE'), ('PASAPORTE', 'PASAPORTE'), ('OTRO', 'OTRO')], default='DNI', max_length=40),
        ),
    ]