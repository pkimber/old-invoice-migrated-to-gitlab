# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
        ('invoice', '0012_auto_20160415_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoicesettings',
            name='time_record_product',
            field=models.ForeignKey(to='stock.Product', help_text='Product used for time records.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='invoiceline',
            name='product',
            field=models.ForeignKey(related_name='+', to='stock.Product'),
        ),
        migrations.AlterUniqueTogether(
            name='invoice',
            unique_together=set([('number', 'deleted_version')]),
        ),
    ]
