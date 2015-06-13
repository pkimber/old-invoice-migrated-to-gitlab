# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import finance.models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0003_auto_20150526_1908'),
        ('invoice', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoicesettings',
            name='vat_number',
        ),
        migrations.RemoveField(
            model_name='invoicesettings',
            name='vat_rate',
        ),
        migrations.AddField(
            model_name='invoiceline',
            name='vat_code',
            field=models.ForeignKey(default=finance.models.legacy_vat_code, related_name='+', to='finance.VatCode'),
        ),
        migrations.AlterField(
            model_name='invoiceline',
            name='vat_rate',
            field=models.DecimalField(help_text='VAT rate when the line was saved.', decimal_places=3, max_digits=5),
        ),
    ]
