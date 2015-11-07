# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0003_auto_20150613_0642'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeRecordCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=100)),
                ('billable', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
                ('icon', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'verbose_name': 'Time Record Category',
                'ordering': ['description', 'billable'],
                'verbose_name_plural': 'Time Record Categories',
            },
        ),
        migrations.AddField(
            model_name='timerecord',
            name='category',
            field=models.ForeignKey(to='invoice.TimeRecordCategory', blank=True, null=True),
        ),
    ]
