# -*- encoding: utf-8 -*-
from datetime import date

from django.test import TestCase

from contact.tests.factories import ContactFactory
from crm.tests.factories import TicketFactory
from finance.tests.factories import VatSettingsFactory
from invoice.models import Invoice
from invoice.service import InvoiceCreateBatch
from invoice.tests.factories import (
    InvoiceContactFactory,
    InvoiceSettingsFactory,
    TimeRecordFactory,
)
from login.tests.factories import UserFactory


class TestInvoiceCreateBatch(TestCase):

    def test_create_invoices(self):
        """Create an invoice"""
        InvoiceSettingsFactory()
        VatSettingsFactory()
        contact = ContactFactory()
        InvoiceContactFactory(contact=contact)
        ticket = TicketFactory(contact=contact)
        TimeRecordFactory(ticket=ticket, date_started=date(2012, 7, 1))
        TimeRecordFactory(ticket=ticket, date_started=date(2012, 8, 1))
        TimeRecordFactory(ticket=ticket)
        # action
        InvoiceCreateBatch().create(UserFactory(), date(2012, 9, 30))
        invoices = Invoice.objects.filter(contact=contact)
        self.assertEquals(1, len(invoices))
        invoice = invoices[0]
        self.assertEquals(2, len(invoice.invoiceline_set.all()))

    def test_create_invoices_only_billable_time(self):
        InvoiceSettingsFactory()
        VatSettingsFactory()
        contact = ContactFactory()
        InvoiceContactFactory(contact=contact)
        ticket = TicketFactory(contact=contact)
        TimeRecordFactory(ticket=ticket, date_started=date(2012, 7, 1))
        InvoiceCreateBatch().create(UserFactory(), date(2012, 9, 30))
        TimeRecordFactory(
            ticket=ticket,
            date_started=date(2012, 7, 1),
            billable=False,
        )
        InvoiceCreateBatch().create(UserFactory(), date(2012, 9, 30))
        self.assertEquals(
            1,
            Invoice.objects.filter(contact=contact).count()
        )

    def test_create_invoices_do_not_bill_twice(self):
        """Check we can't include the time records more than once"""
        InvoiceSettingsFactory()
        VatSettingsFactory()
        contact = ContactFactory()
        InvoiceContactFactory(contact=contact)
        ticket = TicketFactory(contact=contact)
        TimeRecordFactory(ticket=ticket, date_started=date(2012, 7, 1))
        user = UserFactory()
        InvoiceCreateBatch().create(user, date(2012, 9, 30))
        self.assertEquals(
            1,
            Invoice.objects.filter(contact=contact).count()
        )
        InvoiceCreateBatch().create(user, date(2012, 9, 30))
        self.assertEquals(
            1,
            Invoice.objects.filter(contact=contact).count()
        )
