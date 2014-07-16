# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from .factories import (
    InvoiceFactory,
    InvoiceLineFactory,
)


class TestCreditNote(TestCase):

    def test_factory(self):
        """ Create a simple credit note."""
        invoice = InvoiceFactory()
        InvoiceLineFactory(invoice=invoice, price=Decimal('10.01'))
        InvoiceLineFactory(invoice=invoice, price=Decimal('0.99'))
        self.assertEqual(Decimal('11.00'), invoice.net)

    def test_no_negative_price(self):
        invoice = InvoiceFactory()
        line = InvoiceLineFactory(invoice=invoice, price=Decimal('-10.01'))
        self.assertRaises(
            ValidationError,
            line.full_clean,
        )

    def test_allow_negative_quantity(self):
        invoice = InvoiceFactory()
        line = InvoiceLineFactory(
            invoice=invoice,
            price=Decimal('1.01'),
            quantity=Decimal('-1'),
        )
        line.full_clean()
        self.assertEqual(Decimal('-1.01'), invoice.net)
