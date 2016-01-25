# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models

def _create_contact_invoice(contact, hourly_rate, model):
    try:
        model.objects.get(contact=contact)
    except model.DoesNotExist:
        obj = model(**dict(
            contact=contact,
            hourly_rate=hourly_rate,
        ))
        obj.save()
        obj.full_clean()


def _create(pk, model_contact_old, model_contact_new, model_contact_invoice):
    contact_old = model_contact_old.objects.get(pk=pk)
    hourly_rate = contact_old.hourly_rate
    contact_new = model_contact_new.objects.get(slug=contact_old.slug)
    _create_contact_invoice(contact_new, hourly_rate, model_contact_invoice)


def transfer_to_new_contact_app(apps, schema_editor):
    model_contact_invoice = apps.get_model('invoice', 'InvoiceContact')
    model_contact_new = apps.get_model(settings.CONTACT_MODEL)
    model_contact_old = apps.get_model('crm', 'Contact')
    pks = [obj.pk for obj in model_contact_old.objects.all().order_by('pk')]
    for pk in pks:
        _create(pk, model_contact_old, model_contact_new, model_contact_invoice)


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0005_auto_20160125_1134'),
        migrations.swappable_dependency(settings.CONTACT_MODEL),
    ]

    operations = [
        migrations.RunPython(transfer_to_new_contact_app),
    ]
