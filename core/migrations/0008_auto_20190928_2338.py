# Generated by Django 2.2.4 on 2019-09-28 23:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('core', '0007_auto_20190927_1036'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatoDeContacto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('teléfono', 'teléfono'), ('email', 'email'), ('web', 'web'), ('twitter', 'twitter'), ('facebook', 'facebook'), ('instagram', 'instagram'), ('youtube', 'youtube'), ('skype', 'skype')], max_length=20)),
                ('valor', models.CharField(max_length=100)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'unique_together': {('tipo', 'valor', 'content_type', 'object_id')},
            },
        ),
        migrations.RemoveField(
            model_name='obrasocialpaciente',
            name='obra_social',
        ),
        migrations.RemoveField(
            model_name='obrasocialpaciente',
            name='paciente',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='carpeta_familiar',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='obras_sociales',
        ),
        migrations.DeleteModel(
            name='CarpetaFamiliar',
        ),
        migrations.DeleteModel(
            name='ObraSocial',
        ),
        migrations.DeleteModel(
            name='ObraSocialPaciente',
        ),
        migrations.DeleteModel(
            name='Paciente',
        ),
    ]
