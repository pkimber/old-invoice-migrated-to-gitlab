# -*- encoding: utf-8 -*-
from datetime import date

from django.test import TestCase

from invoice.models import InvoiceError
from invoice.service import (
    InvoiceCreate,
    InvoicePrint,
)
from crm.tests.factories import (
    ContactFactory,
    TicketFactory,
)
from finance.tests.factories import VatSettingsFactory
from invoice.tests.factories import (
    InvoiceFactory,
    InvoiceLineFactory,
    InvoiceSettingsFactory,
    TimeRecordFactory,
)
from login.tests.factories import UserFactory


class TestInvoicePrint(TestCase):

    def test_invoice_create_pdf(self):
        InvoiceSettingsFactory()
        VatSettingsFactory()
        contact = ContactFactory()
        ticket = TicketFactory(contact=contact)
        TimeRecordFactory(ticket=ticket, date_started=date(2013, 12, 1))
        invoice = InvoiceCreate().create(
            UserFactory(),
            contact,
            date(2013, 12, 31)
        )
        InvoicePrint().create_pdf(invoice, None)

    def test_invoice_create_pdf_no_lines(self):
        """Cannot create a PDF if the invoice has no lines"""
        invoice = InvoiceFactory()
        self.assertRaises(
            InvoiceError,
            InvoicePrint().create_pdf,
            invoice,
            None
        )

    def test_invoice_create_pdf_not_draft(self):
        """Cannot create a PDF if the invoice has already been printed"""
        InvoiceSettingsFactory()
        VatSettingsFactory()
        invoice = InvoiceFactory()
        InvoiceLineFactory(invoice=invoice)
        InvoicePrint().create_pdf(invoice, None)
        self.assertRaises(
            InvoiceError,
            InvoicePrint().create_pdf,
            invoice,
            None
        )
