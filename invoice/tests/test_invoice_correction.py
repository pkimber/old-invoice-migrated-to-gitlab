# -*- encoding: utf-8 -*-
from datetime import date
from dateutil.relativedelta import relativedelta

from django.test import TestCase

from invoice.models import InvoiceError
from invoice.service import (
    InvoiceCreate,
    InvoicePrint,
)
from invoice.tests.factories import (
    InvoiceLineFactory,
    InvoiceSettingsFactory,
    TimeRecordFactory,
)

class TestInvoiceCorrection(TestCase):

    def test_is_not_draft(self):
        InvoiceSettingsFactory()
        tr = TimeRecordFactory()
        invoice = InvoiceCreate().create(
            tr.user, tr.ticket.contact, date.today()
        )
        self.assertTrue(invoice.is_draft)
        InvoicePrint().create_pdf(invoice, None)
        self.assertFalse(invoice.is_draft)

    def test_set_is_draft(self):
        InvoiceSettingsFactory()
        tr = TimeRecordFactory()
        invoice = InvoiceCreate().create(
            tr.user, tr.ticket.contact, date.today()
        )
        self.assertTrue(invoice.is_draft)
        InvoicePrint().create_pdf(invoice, None)
        self.assertFalse(invoice.is_draft)
        invoice.set_to_draft()
        self.assertTrue(invoice.is_draft)

    def test_set_is_draft_too_late(self):
        """invoice can only be set back to draft on the day it is created."""
        InvoiceSettingsFactory()
        tr = TimeRecordFactory()
        TimeRecordFactory(ticket = tr.ticket)
        invoice = InvoiceCreate().create(
            tr.user, tr.ticket.contact, date.today()
        )
        invoice.invoice_date=date.today() + relativedelta(days=-1)
        invoice.save()
        self.assertTrue(invoice.is_draft)
        InvoicePrint().create_pdf(invoice, None)
        self.assertFalse(invoice.is_draft)
        with self.assertRaises(InvoiceError):
            invoice.set_to_draft()

    def test_remove_time_lines(self):
        """Remove all lines (because they are all linked to time records)."""
        InvoiceSettingsFactory()
        tr = TimeRecordFactory()
        TimeRecordFactory(ticket=tr.ticket)
        invoice = InvoiceCreate().create(
            tr.user, tr.ticket.contact, date.today()
        )
        self.assertTrue(invoice.is_draft)
        InvoicePrint().create_pdf(invoice, None)
        self.assertTrue(invoice.has_lines)
        invoice.set_to_draft()
        invoice.remove_time_lines()
        self.assertFalse(invoice.has_lines)

    def test_remove_time_lines_not_extra(self):
        """Remove all but one line.

        The extra line is not removed because it isn't linked to a time record.

        """
        InvoiceSettingsFactory()
        tr = TimeRecordFactory()
        TimeRecordFactory(ticket=tr.ticket)
        invoice = InvoiceCreate().create(
            tr.user, tr.ticket.contact, date.today()
        )
        extra_line = InvoiceLineFactory(invoice=invoice)
        self.assertTrue(invoice.is_draft)
        InvoicePrint().create_pdf(invoice, None)
        self.assertTrue(invoice.has_lines)
        invoice.set_to_draft()
        invoice.remove_time_lines()
        self.assertListEqual(
            [extra_line.pk,],
            [i.pk for i in invoice.invoiceline_set.all()]
        )

    def test_refresh(self):
        """Create a draft invoice, and then add more time records to it."""
        InvoiceSettingsFactory()
        tr = TimeRecordFactory()
        invoice = InvoiceCreate().create(
            tr.user, tr.ticket.contact, date.today()
        )
        self.assertEqual(1, invoice.invoiceline_set.count())
        # create a couple more time records which can be added
        TimeRecordFactory(ticket=tr.ticket)
        TimeRecordFactory(ticket=tr.ticket)
        InvoiceCreate().refresh(tr.user, invoice, date.today())
        self.assertEqual(3, invoice.invoiceline_set.count())

    def test_refresh_draft_only(self):
        """Only draft invoices can be refreshed."""
        InvoiceSettingsFactory()
        tr = TimeRecordFactory()
        invoice = InvoiceCreate().create(
            tr.user, tr.ticket.contact, date.today()
        )
        self.assertEqual(1, invoice.invoiceline_set.count())
        InvoicePrint().create_pdf(invoice, None)
        with self.assertRaises(InvoiceError):
            InvoiceCreate().refresh(tr.user, invoice, date.today())
