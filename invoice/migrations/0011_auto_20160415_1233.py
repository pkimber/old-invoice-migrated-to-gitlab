# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stock', '0001_initial'),
        ('invoice', '0010_auto_20160125_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='date_deleted',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='invoice',
            name='deleted_version',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='invoice',
            name='number',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='invoice',
            name='user_deleted',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, related_name='+', null=True),
        ),
        migrations.AddField(
            model_name='invoiceline',
            name='product',
            field=models.ForeignKey(to='stock.Product', blank=True, related_name='+', null=True),
        ),
    ]
