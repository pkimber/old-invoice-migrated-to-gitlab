# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0004_auto_20151107_2230'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quicktimerecord',
            options={'ordering': ['-chargeable', 'description'], 'verbose_name_plural': 'Quick Time Recording', 'verbose_name': 'Quick Time Recording'},
        ),
        migrations.RenameField(
            model_name='invoice',
            old_name='contact',
            new_name='crm_contact',
        ),
    ]
