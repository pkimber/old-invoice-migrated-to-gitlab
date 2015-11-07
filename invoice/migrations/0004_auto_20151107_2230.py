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
            name='QuickTimeRecord',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('chargeable', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=100)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Quick Time Recording',
                'ordering': ['description', 'chargeable'],
                'verbose_name_plural': 'Quick Time Recording',
            },
        ),
        migrations.CreateModel(
            name='TimeCode',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=100)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Time Code',
                'ordering': ['description'],
                'verbose_name_plural': 'Time Codes',
            },
        ),
        migrations.AddField(
            model_name='quicktimerecord',
            name='time_code',
            field=models.ForeignKey(to='invoice.TimeCode'),
        ),
        migrations.AddField(
            model_name='quicktimerecord',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='timerecord',
            name='time_code',
            field=models.ForeignKey(to='invoice.TimeCode', blank=True, null=True),
        ),
    ]
