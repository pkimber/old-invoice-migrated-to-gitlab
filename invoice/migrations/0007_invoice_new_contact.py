# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_default_gender'),
        ('invoice', '0006_auto_20160125_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='new_contact',
            field=models.ForeignKey(blank=True, to='contact.Contact', related_name='invoice_contact', null=True),
        ),
    ]
