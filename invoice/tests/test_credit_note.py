# -*- encoding: utf-8 -*-
from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from finance.tests.factories import VatSettingsFactory
from invoice.models import InvoiceError
from invoice.service import (
    InvoiceCreate,
    InvoicePrint,
)
from .factories import (
    InvoiceContactFactory,
    InvoiceFactory,
    InvoiceLineFactory,
    InvoiceSettingsFactory,
)


class TestCreditNote(TestCase):

    def _credit_note(self):
        InvoiceSettingsFactory()
        VatSettingsFactory()
        credit_note = InvoiceFactory()
        credit_note.full_clean()
        line = InvoiceLineFactory(
            invoice=credit_note,
            price=Decimal('1.01'),
            quantity=Decimal('-1'),
        )
        line.full_clean()
        return credit_note

    def test_factory(self):
        """ Create a simple credit note."""
        credit_note = InvoiceFactory()
        credit_note.full_clean()
        InvoiceLineFactory(invoice=credit_note, price=Decimal('10.01'))
        line = InvoiceLineFactory(invoice=credit_note, price=Decimal('0.99'))
        line.full_clean()
        self.assertEqual(Decimal('11.00'), credit_note.net)

    def test_no_negative_price(self):
        invoice = InvoiceFactory()
        line = InvoiceLineFactory(invoice=invoice, price=Decimal('-10.01'))
        self.assertRaises(
            ValidationError,
            line.full_clean,
        )

    def test_allow_negative_quantity(self):
        credit_note = self._credit_note()
        self.assertEqual(Decimal('-1.01'), credit_note.net)

    def test_description(self):
        credit_note = self._credit_note()
        self.assertEqual('Credit Note', credit_note.description)

    def test_credit_note(self):
        credit = self._credit_note()
        InvoiceContactFactory(contact=credit.contact)
        InvoiceCreate().create(credit.user, credit.contact, date.today())

    def test_line_is_credit(self):
        credit = self._credit_note()
        line = InvoiceLineFactory(
            invoice=credit,
            price=Decimal('0.02'),
            quantity=Decimal('-1'),
        )
        self.assertTrue(line.is_credit)

    def test_print_only_negative(self):
        credit = self._credit_note()
        InvoicePrint().create_pdf(credit, None)

    def test_print_not_negative_and_positive(self):
        credit = self._credit_note()
        InvoiceLineFactory(
            invoice=credit,
            price=Decimal('2.02'),
            quantity=Decimal('1'),
        )
        self.assertRaises(
            InvoiceError,
            InvoicePrint().create_pdf,
            credit,
            None,
        )
