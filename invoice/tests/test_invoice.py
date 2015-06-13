# -*- encoding: utf-8 -*-
"""
Test invoice.
"""
from decimal import Decimal

from django.test import TestCase

from finance.tests.factories import VatSettingsFactory
from invoice.models import InvoiceLine
from invoice.service import InvoicePrint
from invoice.tests.factories import (
    InvoiceFactory,
    InvoiceLineFactory,
    InvoiceSettingsFactory,
    TimeRecordFactory,
)


class TestInvoice(TestCase):

    def test_create(self):
        """ Create a simple invoice """
        invoice = InvoiceFactory()
        invoice.full_clean()
        invoice.save()
        self.assertGreater(invoice.pk, 0)

    def test_create_with_lines(self):
        """ Create a simple invoice with lines """
        VatSettingsFactory()
        invoice = InvoiceFactory()
        line = InvoiceLineFactory(
            invoice=invoice,
            quantity=Decimal('1.3'),
            units='hours',
            price=Decimal('300.00'),
        )
        line = InvoiceLineFactory(
            invoice=invoice,
            quantity=Decimal('2.4'),
            units='hours',
            price=Decimal('200.23'),
        )
        self.assertGreater(invoice.pk, 0)
        self.assertEqual(Decimal('870.55'), invoice.net)
        self.assertEqual(Decimal('1044.66'), invoice.gross)
        self.assertFalse(line.is_credit)

    def test_description(self):
        invoice = InvoiceFactory()
        self.assertEquals('Invoice', invoice.description)

    def test_get_first_line_number(self):
        """get the number for the first invoice line"""
        invoice = InvoiceFactory()
        self.assertEqual(1, invoice.get_next_line_number())

    def test_get_next_line_number(self):
        """get the number for the next invoice line"""
        invoice = InvoiceFactory()
        InvoiceLineFactory(invoice=invoice, line_number=1)
        InvoiceLineFactory(invoice=invoice, line_number=2)
        self.assertEqual(3, invoice.get_next_line_number())

    def test_get_next_line_number_fill_gap(self):
        """get the number for the next invoice line"""
        invoice = InvoiceFactory()
        InvoiceLineFactory(invoice=invoice, line_number=1)
        InvoiceLineFactory(invoice=invoice, line_number=2)
        InvoiceLineFactory(invoice=invoice, line_number=4)
        self.assertEqual(3, invoice.get_next_line_number())

    def test_get_next_line_number_two_invoices(self):
        """get the number for the next invoice line"""
        invoice_1 = InvoiceFactory()
        InvoiceLineFactory(invoice=invoice_1, line_number=1)
        InvoiceLineFactory(invoice=invoice_1, line_number=2)
        invoice_2 = InvoiceFactory()
        InvoiceLineFactory(invoice=invoice_2, line_number=1)
        self.assertEqual(3, invoice_1.get_next_line_number())
        self.assertEqual(2, invoice_2.get_next_line_number())

    def test_has_lines(self):
        """does the invoice have any lines"""
        invoice = InvoiceFactory()
        InvoiceLineFactory(
            invoice=invoice,
            quantity=Decimal('1.3'),
            units='hours',
            price=Decimal('300.00'),
        )
        self.assertTrue(invoice.has_lines)

    def test_has_lines_not(self):
        invoice = InvoiceFactory()
        self.assertFalse(invoice.has_lines)

    def test_user_can_edit(self):
        line = InvoiceLineFactory()
        self.assertTrue(line.user_can_edit)

    def test_user_can_edit_has_time(self):
        line = InvoiceLineFactory()
        TimeRecordFactory(invoice_line=line)
        self.assertFalse(line.user_can_edit)

    def test_user_can_edit_invoice(self):
        InvoiceSettingsFactory()
        VatSettingsFactory()
        invoice = InvoiceFactory()
        line = InvoiceLineFactory(invoice=invoice)
        TimeRecordFactory(invoice_line=line)
        InvoicePrint().create_pdf(invoice, None)
        # refresh
        line = InvoiceLine.objects.get(pk=line.pk)
        self.assertFalse(line.user_can_edit)
