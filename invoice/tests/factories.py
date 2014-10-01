# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import factory

from datetime import date
from decimal import Decimal

from dateutil.relativedelta import relativedelta

from django.utils import timezone

from crm.tests.factories import (
    ContactFactory,
    TicketFactory,
)
from login.tests.factories import UserFactory

from invoice.models import (
    Invoice,
    InvoiceLine,
    InvoiceSettings,
    TimeRecord,
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
    def description(n):
        return 'description_{}'.format(n)

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


class TimeRecordFactory(factory.django.DjangoModelFactory):

    billable = True
    date_started = date.today()
    start_time = timezone.now()
    ticket = factory.SubFactory(TicketFactory)

    class Meta:
        model = TimeRecord

    @factory.lazy_attribute
    def end_time(self):
        return self.start_time + relativedelta(hours=1)

    @factory.lazy_attribute
    def user(self):
        return self.ticket.user
