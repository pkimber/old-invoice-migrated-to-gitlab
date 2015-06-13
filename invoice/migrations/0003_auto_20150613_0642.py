# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0002_auto_20150526_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoiceline',
            name='vat_code',
            field=models.ForeignKey(related_name='+', to='finance.VatCode'),
        ),
    ]
