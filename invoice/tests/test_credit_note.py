# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

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
