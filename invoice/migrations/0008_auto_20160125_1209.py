# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


def _update(obj, model_contact_old, model_contact_new):
    contact_old = model_contact_old.objects.get(pk=obj.contact_id)
    contact_new = model_contact_new.objects.get(slug=contact_old.slug)
    obj.new_contact = contact_new
    obj.save()


def transfer_to_new_contact_app(apps, schema_editor):
    model_invoice = apps.get_model('invoice', 'Invoice')
    model_contact_new = apps.get_model(settings.CONTACT_MODEL)
    # try:
    model_contact_old = apps.get_model('crm', 'Contact')
    pks = [obj.pk for obj in model_invoice.objects.all().order_by('pk')]
    for pk in pks:
        invoice = model_invoice.objects.get(pk=pk)
        _update(invoice, model_contact_old, model_contact_new)
    # except LookupError:
    #     print(
    #         "Warning: Cannot find 'crm.Contact'.  If you have an old "
    #         "'Contact' table in 'crm', it will not be updated."
    #     )


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0007_invoice_new_contact'),
        migrations.swappable_dependency(settings.CONTACT_MODEL),
    ]

    operations = [
        migrations.RunPython(transfer_to_new_contact_app),
    ]
