# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import factory

from datetime import date

from crm.tests.factories import ContactFactory
from login.tests.factories import UserFactory

from invoice.models import Invoice


class InvoiceFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Invoice

    contact = factory.SubFactory(ContactFactory)
    invoice_date = date.today()
    user = factory.SubFactory(UserFactory)
