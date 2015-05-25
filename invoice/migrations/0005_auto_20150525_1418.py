# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0004_auto_20150525_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoiceline',
            name='vat_code',
            field=models.ForeignKey(related_name='+', to='invoice.VatCode'),
        ),
    ]
