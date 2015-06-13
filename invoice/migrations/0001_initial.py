# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        migrations.swappable_dependency(settings.CONTACT_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('invoice_date', models.DateField()),
                ('pdf', models.FileField(storage=django.core.files.storage.FileSystemStorage(location='media-private'), upload_to='invoice/%Y/%m/%d', blank=True)),
                ('contact', models.ForeignKey(to=settings.CONTACT_MODEL)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['pk'],
                'verbose_name': 'Invoice',
                'verbose_name_plural': 'Invoices',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InvoiceLine',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('line_number', models.IntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('quantity', models.DecimalField(max_digits=6, decimal_places=2)),
                ('units', models.CharField(max_length=5)),
                ('price', models.DecimalField(max_digits=8, decimal_places=2)),
                ('net', models.DecimalField(max_digits=8, decimal_places=2)),
                ('vat_rate', models.DecimalField(max_digits=5, decimal_places=3)),
                ('vat', models.DecimalField(max_digits=8, decimal_places=2)),
                ('invoice', models.ForeignKey(to='invoice.Invoice')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['line_number'],
                'verbose_name': 'Invoice line',
                'verbose_name_plural': 'Invoice lines',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InvoiceSettings',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('vat_rate', models.DecimalField(help_text='e.g. 0.175 to charge VAT at 17.5 percent', decimal_places=2, max_digits=8)),
                ('vat_number', models.CharField(blank=True, max_length=12)),
                ('name_and_address', models.TextField()),
                ('phone_number', models.CharField(max_length=100)),
                ('footer', models.TextField()),
            ],
            options={
                'verbose_name': 'Invoice print settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TimeRecord',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('date_started', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('billable', models.BooleanField(default=False)),
                ('invoice_line', models.OneToOneField(to='invoice.InvoiceLine', blank=True, null=True)),
                ('ticket', models.ForeignKey(to='crm.Ticket')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_started', '-start_time'],
                'verbose_name': 'Time record',
                'verbose_name_plural': 'Time records',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='invoiceline',
            unique_together=set([('invoice', 'line_number')]),
        ),
    ]
