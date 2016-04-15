# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models


def _init_product(model, product_category):
    try:
        obj = model.objects.get(slug='migration')
    except model.DoesNotExist:
        obj = model(**dict(
            slug='migration',
            name='Migration',
            description='Initial Migration',
            price=Decimal('0'),
            category=product_category,
        ))
        obj.save()
        obj.full_clean()
    return obj


def _init_product_category(model, product_type):
    try:
        obj = model.objects.get(slug='system')
    except model.DoesNotExist:
        obj = model(**dict(
            slug='system',
            name='System',
            product_type=product_type,
        ))
        obj.save()
        obj.full_clean()
    return obj


def _init_product_type(model):
    try:
        obj = model.objects.get(slug='system')
    except model.DoesNotExist:
        obj = model(**dict(
            slug='system',
            name='System',
        ))
        obj.save()
        obj.full_clean()
    return obj


def _init_invoice(invoice_model):
    pks = [obj.pk for obj in invoice_model.objects.all()]
    for pk in pks:
        obj = invoice_model.objects.get(pk=pk)
        obj.number = obj.pk
        obj.save()


def _init_invoice_line(invoice_line_model,
        product_type_model, product_category_model, product_model):
    product = product_model.objects.exclude(legacy=True).last()
    if not product:
        product_type = _init_product_type(product_type_model)
        product_category = _init_product_category(product_category_model, product_type)
        product = _init_product(product_model, product_category)
    pks = [line.pk for line in invoice_line_model.objects.all()]
    for pk in pks:
        line = invoice_line_model.objects.get(pk=pk)
        line.product = product
        line.save()


def default_state(apps, schema_editor):
    invoice_line_model = apps.get_model('invoice', 'InvoiceLine')
    invoice_model = apps.get_model('invoice', 'Invoice')
    product_category_model = apps.get_model('stock', 'ProductCategory')
    product_model = apps.get_model('stock', 'Product')
    product_type_model = apps.get_model('stock', 'ProductType')
    _init_invoice(invoice_model)
    _init_invoice_line(
        invoice_line_model,
        product_type_model,
        product_category_model,
        product_model,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0011_auto_20160415_1233'),
    ]

    operations = [
        migrations.RunPython(default_state),
    ]
