# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import factory

from datetime import date
from decimal import Decimal

from crm.tests.factories import ContactFactory
from login.tests.factories import UserFactory

from invoice.models import (
    Invoice,
    InvoiceLine,
    InvoiceSettings,
)


class InvoiceFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Invoice

    contact = factory.SubFactory(ContactFactory)
    invoice_date = date.today()
    user = factory.SubFactory(UserFactory)


class InvoiceLineFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = InvoiceLine

    price = 0
    quantity = 1
    units = 'each'
    vat_rate = 20

    @factory.sequence
    def line_number(n):
        return n

    @factory.lazy_attribute
    def user(self):
        return self.invoice.user


class InvoiceSettingsFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = InvoiceSettings

    vat_rate = Decimal('20')
