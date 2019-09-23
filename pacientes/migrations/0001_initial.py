# Generated by Django 2.2.4 on 2019-09-22 20:35

import address.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0002_auto_20160213_1726'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarpetaFamiliar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_familia', models.CharField(choices=[('nuclear', 'Nuclear'), ('nuclear_ampliada', 'Nuclear Ampliada'), ('binuclear', 'Binuclear'), ('monoparental', 'Monoparental'), ('extensa', 'Extensa'), ('unipersonal', 'Unipersonal'), ('equivalentes', 'Equivalentes Familiares')], max_length=50)),
                ('apellido_principal', models.CharField(max_length=100)),
                ('direccion', address.models.AddressField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='address.Address')),
            ],
            options={
                'verbose_name': 'Carpeta familiar',
                'verbose_name_plural': 'Carpetas familiares',
            },
        ),
        migrations.CreateModel(
            name='ObraSocial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('codigo', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'Obra Social',
                'verbose_name_plural': 'Obras Sociales',
            },
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=50)),
                ('apellido', models.CharField(default='', editable=False, max_length=30)),
                ('sexo', models.CharField(choices=[('masculino', 'masculino'), ('femenino', 'femenino'), ('otro', 'otro')], default='', max_length=20)),
                ('fecha_nacimiento', models.DateField(default=datetime.date(2019, 9, 22))),
                ('tipo_documento', models.CharField(choices=[('DNI', 'DNI'), ('LC', 'LC'), ('LE', 'LE'), ('PASAPORTE', 'PASAPORTE'), ('OTRO', 'OTRO')], default='DNI', max_length=20)),
                ('numero_documento', models.CharField(blank=True, help_text='Deje en blanco si está indocumentado', max_length=30, null=True)),
                ('nacionalidad', models.CharField(choices=[('argentina', 'argentina'), ('boliviana', 'boliviana'), ('brasilera', 'brasilera'), ('chilena', 'chilena'), ('colombiana', 'colombiana'), ('ecuatoriana', 'ecuatoriana'), ('paraguaya', 'paraguaya'), ('peruana', 'peruana'), ('uruguaya', 'uruguaya'), ('venezolana', 'venezolana'), ('otra', 'otra')], default='argentina', max_length=50)),
                ('vinculo', models.CharField(choices=[('Padre', 'Padre'), ('Hijo/a', 'Hijo/a'), ('Madre', 'Madre'), ('Abuelo/a', 'Abuelo/a'), ('Primo/a', 'Primo/a'), ('Nuera/Yerno', 'Nuera/Yerno'), ('Nieto/a', 'Nieto/a'), ('Cuñado/a', 'Cuñado/a'), ('Concuñado/a', 'Concuñado/a'), ('Tio/a', 'Tio/a'), ('Sobrino/a', 'Sobrino/a'), ('Esposo/a', 'Esposo/a')], help_text='Relación parental relativa a jefe de familia', max_length=50, null=True)),
                ('es_jefe_familia', models.BooleanField(default=False)),
                ('grupo_sanguineo', models.CharField(choices=[('0-', '0-'), ('0+', '0+'), ('A-', 'A-'), ('A+', 'A+'), ('B-', 'B-'), ('B+', 'B+'), ('AB-', 'AB-'), ('AB+', 'AB+')], max_length=20, null=True)),
                ('observaciones', models.TextField()),
                ('carpeta_familiar', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='miembros', to='pacientes.CarpetaFamiliar')),
                ('obra_social', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pacientes.ObraSocial')),
            ],
            options={
                'verbose_name': 'Paciente',
                'verbose_name_plural': 'Pacientes',
            },
        ),
    ]
