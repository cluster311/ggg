# Generated by Django 2.2.4 on 2019-11-16 15:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profesionales', '0008_auto_20191111_2348'),
    ]

    operations = [
        migrations.AddField(
            model_name='profesional',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
