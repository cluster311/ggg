# Generated by Django 2.2.4 on 2019-11-11 01:11

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_usuarioencentrodesalud_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuarioencentrodesalud',
            name='created',
            field=model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created'),
        ),
        migrations.AddField(
            model_name='usuarioencentrodesalud',
            name='elegido',
            field=models.BooleanField(default=False, help_text='Solo uno puede estar elegido en cada momento'),
        ),
        migrations.AddField(
            model_name='usuarioencentrodesalud',
            name='modified',
            field=model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified'),
        ),
    ]
