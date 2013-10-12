"""
Test invoice.
"""
from datetime import datetime
from decimal import Decimal

from django.test import TestCase

from crm.tests.model_maker import make_contact
from invoice.models import Invoice
from invoice.tests.model_maker import make_invoice
from invoice.tests.model_maker import make_invoice_line
from login.tests.scenario import (
    get_user_staff,
    user_default,
)


class TestInvoice(TestCase):

    def setUp(self):
        self.icl = make_contact('icl', 'ICL')
        user_default()

    def test_create(self):
        """ Create a simple invoice """
        invoice = Invoice(
            user=get_user_staff(),
            invoice_date=datetime.today(),
            contact=self.icl,
        )
        invoice.full_clean()
        invoice.save()
        self.assertEqual(1, invoice.pk)

    def test_create_with_lines(self):
        """ Create a simple invoice with lines """
        invoice = make_invoice(
            user=get_user_staff(),
            invoice_date=datetime.today(),
            contact=self.icl,
        )
        make_invoice_line(invoice, 1, 1.3, 'hours', 300.00, 0.20)
        make_invoice_line(invoice, 2, 2.4, 'hours', 200.23, 0.20)
        self.assertGreater(invoice.pk, 0)
        self.assertEqual(Decimal('1044.66'), invoice.gross)
        self.assertEqual(Decimal('870.55'), invoice.net)

    def test_get_first_line_number(self):
        invoice = make_invoice(
            user=get_user_staff(),
            invoice_date=datetime.today(),
            contact=self.icl,
        )
        self.assertEqual(1, invoice.get_next_line_number())

    def test_get_next_line_number(self):
        invoice = make_invoice(
            user=get_user_staff(),
            invoice_date=datetime.today(),
            contact=self.icl,
        )
        make_invoice_line(invoice, 2, 1.3, 'hours', 300.00, 0.20)
        self.assertEqual(3, invoice.get_next_line_number())

    def test_has_lines(self):
        invoice = make_invoice(
            user=get_user_staff(),
            invoice_date=datetime.today(),
            contact=self.icl,
        )
        make_invoice_line(invoice, 2, 1.3, 'hours', 300.00, 0.20)
        self.assertTrue(invoice.has_lines)

    def test_has_lines_not(self):
        invoice = make_invoice(
            user=get_user_staff(),
            invoice_date=datetime.today(),
            contact=self.icl,
        )
        self.assertFalse(invoice.has_lines)
