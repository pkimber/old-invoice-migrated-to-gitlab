# -*- encoding: utf-8 -*-
from datetime import date
from decimal import Decimal

from django.test import TestCase

from crm.tests.factories import (
    ContactFactory,
    TicketFactory,
)
from invoice.service import (
    InvoiceCreate,
    InvoicePrint,
)
from invoice.tests.factories import (
    InvoiceSettingsFactory,
    TimeRecordFactory,
)


class TestInvoice(TestCase):

    def setUp(self):
        InvoiceSettingsFactory()

    def test_invoice_with_time_records(self):
        contact = ContactFactory()
        ticket = TicketFactory(contact=contact)
        tr1 = TimeRecordFactory(ticket=ticket)
        tr2 = TimeRecordFactory(ticket=ticket)
        invoice = InvoiceCreate().create(
            tr1.user, contact, date.today()
        )
        assert invoice.is_draft
        InvoicePrint().create_pdf(invoice, None)
        assert not invoice.is_draft
        assert Decimal('40.00') == invoice.net

    #def test_invoice_with_time_records_no_end_time(self):
    #    contact = ContactFactory()
    #    ticket = TicketFactory(contact=contact)
    #    tr1 = TimeRecordFactory(ticket=ticket)
    #    tr2 = TimeRecordFactory(ticket=ticket, end_time=None)
    #    tr3 = TimeRecordFactory(ticket=ticket)
    #    invoice = InvoiceCreate().create(
    #        tr1.user, contact, date.today()
    #    )
    #    assert invoice.is_draft
    #    InvoicePrint().create_pdf(invoice, None)
    #    assert not invoice.is_draft
    #    assert Decimal('40.00') == invoice.net
