# -*- encoding: utf-8 -*-
import factory

from datetime import date
from dateutil.relativedelta import relativedelta
from decimal import Decimal

from django.utils import timezone

from contact.tests.factories import ContactFactory
from crm.tests.factories import TicketFactory
from finance.models import VatCode
from login.tests.factories import UserFactory
from invoice.models import (
    Invoice,
    InvoiceContact,
    InvoiceLine,
    InvoiceSettings,
    TimeCode,
    TimeRecord,
    QuickTimeRecord,
)
from stock.tests.factories import ProductFactory


class InvoiceContactFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = InvoiceContact

    contact = factory.SubFactory(ContactFactory)
    hourly_rate = Decimal('20')


class InvoiceFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Invoice

    contact = factory.SubFactory(ContactFactory)
    invoice_date = date.today()
    user = factory.SubFactory(UserFactory)

    @factory.sequence
    def number(n):
        return n + 1


class InvoiceLineFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = InvoiceLine

    invoice = factory.SubFactory(InvoiceFactory)
    price = 0
    product = factory.SubFactory(ProductFactory)
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

    time_record_product = factory.SubFactory(ProductFactory)

    class Meta:
        model = InvoiceSettings


class TimeCodeFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = TimeCode

    @factory.sequence
    def description(n):
        return "description_{}".format(n)


class QuickTimeRecordFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = QuickTimeRecord

    time_code = factory.SubFactory(TimeCodeFactory)
    user = factory.SubFactory(UserFactory)

    @factory.sequence
    def description(n):
        return "description_{}".format(n)


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
