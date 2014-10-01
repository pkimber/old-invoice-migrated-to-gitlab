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
    TimeRecordFactory,
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

    def test_remove_time_lines(self):
        """Remove all lines (because they are all linked to time records)."""
        InvoiceSettingsFactory()
        invoice = InvoiceFactory()
        # two invoice lines with time records
        line_1 = InvoiceLineFactory(invoice=invoice)
        TimeRecordFactory(invoice_line=line_1)
        line_2 = InvoiceLineFactory(invoice=invoice)
        TimeRecordFactory(invoice_line=line_2)
        InvoicePrint().create_pdf(invoice, None)
        self.assertTrue(invoice.has_lines)
        invoice.set_to_draft()
        invoice.remove_time_lines()
        self.assertFalse(invoice.has_lines)

    def test_remove_time_lines_not_extra(self):
        """Remove all but one line.

        Because it is not linked to a time record.

        """
        InvoiceSettingsFactory()
        invoice = InvoiceFactory()
        # two invoice lines with time records
        TimeRecordFactory(invoice_line=InvoiceLineFactory(invoice=invoice))
        TimeRecordFactory(invoice_line=InvoiceLineFactory(invoice=invoice))
        # an extra line which is not linked to a time record.
        extra_line = InvoiceLineFactory(invoice=invoice)
        InvoicePrint().create_pdf(invoice, None)
        self.assertTrue(invoice.has_lines)
        invoice.set_to_draft()
        invoice.remove_time_lines()
        self.assertListEqual(
            [extra_line.pk,],
            [i.pk for i in invoice.invoiceline_set.all()]
        )
