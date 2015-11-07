# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('invoice', '0003_auto_20150613_0642'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeCode',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=100)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Time Code',
                'verbose_name_plural': 'Time Codes',
                'ordering': ['description'],
            },
        ),
        migrations.CreateModel(
            name='TimeRecordingTrigger',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('chargeable', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=100)),
                ('icon', models.CharField(blank=True, max_length=100)),
                ('deleted', models.BooleanField(default=False)),
                ('time_code', models.ForeignKey(to='invoice.TimeCode')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Time Recording Trigger',
                'verbose_name_plural': 'Time Recording Triggers',
                'ordering': ['description', 'chargeable'],
            },
        ),
        migrations.AddField(
            model_name='timerecord',
            name='time_code',
            field=models.ForeignKey(to='invoice.TimeCode', null=True, blank=True),
        ),
    ]
