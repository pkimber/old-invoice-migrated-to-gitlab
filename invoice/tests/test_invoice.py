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


class TestInvoice(TestCase):

    def setUp(self):
        self.icl = make_contact('icl', 'ICL')

    def test_create(self):
        """ Create a simple invoice """
        invoice = Invoice(
            invoice_date=datetime.today(),
            contact=self.icl,
        )
        invoice.full_clean()
        invoice.save()
        self.assertEqual(1, invoice.pk)

    def test_create_with_lines(self):
        """ Create a simple invoice with lines """
        invoice = make_invoice(
            invoice_date=datetime.today(),
            contact=self.icl,
        )
        make_invoice_line(invoice, 1, 1.3, 'hours', 300.00, 0.20)
        make_invoice_line(invoice, 2, 2.4, 'hours', 200.23, 0.20)
        self.assertGreater(invoice.pk, 0)
        self.assertEqual(Decimal('1044.66'), invoice.gross)
        self.assertEqual(Decimal('870.55'), invoice.net)
