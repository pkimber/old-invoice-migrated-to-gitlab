# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.db import models, migrations


def _init_state(model, slug, description, rate, deleted):
    try:
        model.objects.get(slug=slug)
    except model.DoesNotExist:
        instance = model(**dict(
            deleted=deleted,
            description=description,
            rate=rate,
            slug=slug,
        ))
        instance.save()
        instance.full_clean()


def default_state(apps, schema_editor):
    state = apps.get_model('invoice', 'VatCode')
    _init_state(state, 'L', 'Legacy', Decimal('0'), True)
    _init_state(state, 'S', 'Standard', Decimal('0.20'), False)
    _init_state(state, 'Z', 'Zero-Rated (outside the EC)', Decimal('0'), False)


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0002_vatcode'),
    ]

    operations = [
        migrations.RunPython(default_state),
    ]
