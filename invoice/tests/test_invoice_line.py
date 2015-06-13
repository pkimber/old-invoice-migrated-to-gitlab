# -*- encoding: utf-8 -*-
"""
Test invoice line
"""
from django.test import TestCase

from invoice.tests.factories import (
    InvoiceLineFactory,
    TimeRecordFactory,
)


class TestInvoiceLine(TestCase):

    def test_has_time_record_not(self):
        invoice_line = InvoiceLineFactory()
        self.assertFalse(invoice_line.has_time_record)

    def test_has_time_record(self):
        invoice_line = InvoiceLineFactory()
        TimeRecordFactory(invoice_line=invoice_line)
        self.assertTrue(invoice_line.has_time_record)
