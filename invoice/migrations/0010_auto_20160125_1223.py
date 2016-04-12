# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0009_auto_20160125_1220'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice',
            old_name='new_contact',
            new_name='contact',
        ),
    ]
