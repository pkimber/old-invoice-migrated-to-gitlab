# -*- encoding: utf-8 -*-
import factory

from datetime import date

from dateutil.relativedelta import relativedelta

from django.utils import timezone

from crm.tests.factories import (
    ContactFactory,
    TicketFactory,
)
from login.tests.factories import UserFactory
from finance.models import (
    VatCode,
    VatSettings,
)
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

    invoice = factory.SubFactory(InvoiceFactory)
    price = 0
    quantity = 1
    units = 'each'

    @factory.sequence
    def description(n):
        return 'description_{}'.format(n)

    @factory.sequence
    def line_number(n):
        return n

    @factory.lazy_attribute
    def user(self):
        return self.invoice.user

    @factory.lazy_attribute
    def vat_code(self):
        return VatCode.objects.get(slug=VatCode.STANDARD)


class InvoiceSettingsFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = InvoiceSettings


class TimeRecordFactory(factory.django.DjangoModelFactory):

    billable = True
    date_started = date.today()
    start_time = timezone.now()
    ticket = factory.SubFactory(TicketFactory)

    class Meta:
        model = TimeRecord

    @factory.sequence
    def title(n):
        return "Time record {}".format(n)

    @factory.lazy_attribute
    def end_time(self):
        return self.start_time + relativedelta(hours=1)

    @factory.lazy_attribute
    def user(self):
        return self.ticket.user
