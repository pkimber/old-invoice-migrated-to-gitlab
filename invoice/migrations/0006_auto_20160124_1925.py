# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_auto_20160124_1926'),
        ('invoice', '0005_auto_20160124_1921'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvoiceContact',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('hourly_rate', models.DecimalField(blank=True, max_digits=8, decimal_places=2, null=True)),
                ('contact', models.OneToOneField(to=settings.CONTACT_MODEL)),
            ],
            options={
                'verbose_name': 'Invoice Contact',
                'verbose_name_plural': 'Invoice Contacts',
            },
        ),
        migrations.AddField(
            model_name='invoice',
            name='contact',
            field=models.ForeignKey(related_name='invoice_contact', to=settings.CONTACT_MODEL, blank=True, null=True),
        ),
    ]
