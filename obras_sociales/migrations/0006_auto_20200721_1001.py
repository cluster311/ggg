# Generated by Django 2.2.10 on 2020-07-21 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obras_sociales', '0005_auto_20200426_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='obrasocialpaciente',
            name='parentesco',
            field=models.CharField(choices=[('conyugue', 'conyugue'), ('hijo', 'hijo'), ('otro', 'otro')], default='otro', max_length=20),
        ),
        migrations.AddField(
            model_name='obrasocialpaciente',
            name='tipo_beneficiario',
            field=models.CharField(choices=[('titular', 'titular'), ('no titular', 'no titular'), ('adherente', 'adherente')], default='Titular', max_length=20),
        ),
    ]
