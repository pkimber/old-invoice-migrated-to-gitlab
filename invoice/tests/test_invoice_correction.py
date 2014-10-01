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

    def create(self, invoice_date=None):
        """ Create a simple invoice with two lines """
        InvoiceSettingsFactory()
        if invoice_date == None:
            invoice_date = date.today()
        invoice = InvoiceFactory(invoice_date=invoice_date)
        InvoiceLineFactory(invoice=invoice)
        InvoiceLineFactory(invoice=invoice)
        InvoicePrint().create_pdf(invoice, None)
        return invoice

    def test_is_draft(self):
        invoice = self.create()
        self.assertFalse(invoice.is_draft)

    def test_set_is_draft(self):
        invoice = self.create()
        self.assertFalse(invoice.is_draft)
        invoice.set_to_draft()
        self.assertTrue(invoice.is_draft)

    def test_set_is_draft_too_late(self):
        """invoice can only be set back to draft on the day it is created."""
        InvoiceSettingsFactory()
        invoice = self.create(date.today() + relativedelta(days=-1))
        self.assertFalse(invoice.is_draft)
        with self.assertRaises(InvoiceError):
            invoice.set_to_draft()
