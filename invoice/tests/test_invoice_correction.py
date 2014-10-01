# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date
from dateutil.relativedelta import relativedelta

from django.test import TestCase

from invoice.models import InvoiceError
from invoice.service import InvoicePrint
from invoice.tests.factories import (
    InvoiceFactory,
    InvoiceLineFactory,
    InvoiceSettingsFactory,
)

class TestInvoiceCorrection(TestCase):

    def test_is_not_draft(self):
        InvoiceSettingsFactory()
        invoice = InvoiceFactory()
        InvoiceLineFactory(invoice=invoice)
        InvoicePrint().create_pdf(invoice, None)
        self.assertFalse(invoice.is_draft)

    def test_set_is_draft(self):
        InvoiceSettingsFactory()
        invoice = InvoiceFactory()
        InvoiceLineFactory(invoice=invoice)
        InvoicePrint().create_pdf(invoice, None)
        self.assertFalse(invoice.is_draft)
        invoice.set_to_draft()
        self.assertTrue(invoice.is_draft)

    def test_set_is_draft_too_late(self):
        """invoice can only be set back to draft on the day it is created."""
        InvoiceSettingsFactory()
        invoice = InvoiceFactory(
            invoice_date=date.today() + relativedelta(days=-1)
        )
        InvoiceLineFactory(invoice=invoice)
        InvoiceLineFactory(invoice=invoice)
        InvoicePrint().create_pdf(invoice, None)
        self.assertFalse(invoice.is_draft)
        with self.assertRaises(InvoiceError):
            invoice.set_to_draft()
