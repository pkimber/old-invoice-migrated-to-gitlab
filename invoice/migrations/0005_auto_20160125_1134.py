# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_default_gender'),
        ('invoice', '0004_auto_20151107_2230'),
        migrations.swappable_dependency(settings.CONTACT_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InvoiceContact',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('hourly_rate', models.DecimalField(blank=True, decimal_places=2, null=True, max_digits=8)),
                ('contact', models.OneToOneField(to=settings.CONTACT_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Invoice Contacts',
                'verbose_name': 'Invoice Contact',
            },
        ),
        migrations.AlterModelOptions(
            name='quicktimerecord',
            options={'verbose_name_plural': 'Quick Time Recording', 'verbose_name': 'Quick Time Recording', 'ordering': ['-chargeable', 'description']},
        ),
    ]
