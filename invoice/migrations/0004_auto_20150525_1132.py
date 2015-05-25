# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import invoice.models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0003_auto_20150525_1121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoicesettings',
            name='vat_rate',
        ),
        migrations.AddField(
            model_name='invoiceline',
            name='vat_code',
            field=models.ForeignKey(related_name='+', to='invoice.VatCode', default=invoice.models.legacy_vat_code),
        ),
        migrations.AddField(
            model_name='invoicesettings',
            name='vat_standard',
            field=models.ForeignKey(related_name='+', to='invoice.VatCode', default=invoice.models.default_vat_code),
        ),
        migrations.AlterField(
            model_name='invoiceline',
            name='vat_rate',
            field=models.DecimalField(help_text='VAT rate when the line was saved.', max_digits=5, decimal_places=3),
        ),
    ]
