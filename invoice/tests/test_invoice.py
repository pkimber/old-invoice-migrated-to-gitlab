# -*- encoding: utf-8 -*-
import pytest
"""
Test invoice.
"""
from decimal import Decimal

from django.test import TestCase

from finance.tests.factories import VatSettingsFactory
from invoice.models import Invoice, InvoiceLine
from invoice.service import InvoicePrint
from invoice.tests.factories import (
    InvoiceFactory,
    InvoiceLineFactory,
    InvoiceSettingsFactory,
    TimeRecordFactory,
)


@pytest.mark.django_db
def test_create():
    """ Create a simple invoice """
    invoice = InvoiceFactory()
    invoice.full_clean()
    invoice.save()
    assert invoice.pk > 0
    assert invoice.number > 0


@pytest.mark.django_db
def test_create_with_lines():
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
    assert invoice.pk > 0
    assert Decimal('870.55') == invoice.net
    assert Decimal('1044.66') == invoice.gross
    assert line.is_credit is False


@pytest.mark.django_db
def test_description():
    invoice = InvoiceFactory()
    assert 'Invoice' == invoice.description


@pytest.mark.django_db
def test_get_first_line_number():
    """get the number for the first invoice line"""
    invoice = InvoiceFactory()
    assert 1 == invoice.get_next_line_number()


@pytest.mark.django_db
def test_get_next_line_number():
    """get the number for the next invoice line"""
    invoice = InvoiceFactory()
    InvoiceLineFactory(invoice=invoice, line_number=1)
    InvoiceLineFactory(invoice=invoice, line_number=2)
    assert 3 == invoice.get_next_line_number()


@pytest.mark.django_db
def test_get_next_line_number_fill_gap():
    """get the number for the next invoice line"""
    invoice = InvoiceFactory()
    InvoiceLineFactory(invoice=invoice, line_number=1)
    InvoiceLineFactory(invoice=invoice, line_number=2)
    InvoiceLineFactory(invoice=invoice, line_number=4)
    assert 3 == invoice.get_next_line_number()


@pytest.mark.django_db
def test_get_next_line_number_two_invoices():
    """get the number for the next invoice line"""
    invoice_1 = InvoiceFactory()
    InvoiceLineFactory(invoice=invoice_1, line_number=1)
    InvoiceLineFactory(invoice=invoice_1, line_number=2)
    invoice_2 = InvoiceFactory()
    InvoiceLineFactory(invoice=invoice_2, line_number=1)
    assert 3 == invoice_1.get_next_line_number()
    assert 2 == invoice_2.get_next_line_number()


@pytest.mark.django_db
def test_has_lines():
    """does the invoice have any lines"""
    invoice = InvoiceFactory()
    InvoiceLineFactory(
        invoice=invoice,
        quantity=Decimal('1.3'),
        units='hours',
        price=Decimal('300.00'),
    )
    assert invoice.has_lines is True


@pytest.mark.django_db
def test_has_lines_not():
    invoice = InvoiceFactory()
    assert invoice.has_lines is False


@pytest.mark.django_db
def test_next_number():
    InvoiceFactory(number=99)
    assert 100 == Invoice.objects.next_number()


@pytest.mark.django_db
def test_next_number():
    InvoiceFactory(number=99, deleted=True)
    InvoiceFactory(number=98, deleted_version=1)
    assert 1 == Invoice.objects.next_number()


@pytest.mark.django_db
def test_user_can_edit():
    line = InvoiceLineFactory()
    assert line.user_can_edit is True


@pytest.mark.django_db
def test_user_can_edit_has_time():
    line = InvoiceLineFactory()
    TimeRecordFactory(invoice_line=line)
    assert line.user_can_edit is False


@pytest.mark.django_db
def test_user_can_edit_invoice():
    InvoiceSettingsFactory()
    VatSettingsFactory()
    invoice = InvoiceFactory()
    line = InvoiceLineFactory(invoice=invoice)
    TimeRecordFactory(invoice_line=line)
    InvoicePrint().create_pdf(invoice, None)
    # refresh
    line = InvoiceLine.objects.get(pk=line.pk)
    assert line.user_can_edit is False
