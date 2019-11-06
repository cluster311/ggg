# Generated by Django 2.2.4 on 2019-11-06 02:42

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20190928_2338'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppLogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('severity', models.PositiveSmallIntegerField(default=0)),
                ('code', models.CharField(max_length=120)),
                ('description', models.TextField(blank=True, null=True)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
        ),
    ]
