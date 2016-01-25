# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import migrations, models


def _update_contact(model, obj, hourly_rate):
    try:
        model.objects.get(contact=obj.pk)
    except model.DoesNotExist:
        obj = model(**dict(
            contact=obj,
            hourly_rate=hourly_rate,
        ))
        obj.save()
        obj.full_clean()


def transfer_to_new_contact_app(apps, schema_editor):
    contact_model = apps.get_model(settings.CONTACT_MODEL)
    crm_contact_model = apps.get_model('crm', 'Contact')
    invoice_contact_model = apps.get_model('invoice', 'InvoiceContact')
    invoice_model = apps.get_model('invoice', 'Invoice')
    pks = [obj.pk for obj in invoice_model.objects.all()]
    for pk in pks:
        invoice = invoice_model.objects.get(pk=pk)
        crm_contact = crm_contact_model.objects.get(pk=invoice.crm_contact.pk)
        hourly_rate = crm_contact.hourly_rate
        contact = contact_model.objects.get(slug=crm_contact.slug)
        invoice.contact = contact
        invoice.save()
        _update_contact(invoice_contact_model, contact, hourly_rate)


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_auto_20160124_1926'),
        ('invoice', '0006_auto_20160124_1925'),
    ]

    operations = [
        migrations.RunPython(transfer_to_new_contact_app),
    ]
