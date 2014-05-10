# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

"""
Test invoice.
"""
from datetime import datetime
from decimal import Decimal

from django.test import TestCase

from invoice.models import Invoice
from invoice.tests.model_maker import make_invoice
from invoice.tests.model_maker import make_invoice_line
from crm.tests.scenario import (
    default_scenario_crm,
    get_contact_farm,
)
from invoice.service import (
    InvoicePrint,
)
from invoice.tests.scenario import (
    default_scenario_invoice,
    get_invoice_line_paperwork_has_time,
    get_invoice_line_paperwork_no_time,
    get_invoice_paperwork,
    invoice_settings,
)
from login.tests.scenario import (
    default_scenario_login,
    get_user_staff,
    user_contractor,
)


class TestInvoice(TestCase):

    def setUp(self):
        user_contractor()
        default_scenario_login()
        default_scenario_crm()
        default_scenario_invoice()
        self.farm = get_contact_farm()

    def test_create(self):
        """ Create a simple invoice """
        invoice = Invoice(
            user=get_user_staff(),
            invoice_date=datetime.today(),
            contact=self.farm,
        )
        invoice.full_clean()
        invoice.save()
        self.assertGreater(invoice.pk, 0)

    def test_create_with_lines(self):
        """ Create a simple invoice with lines """
        invoice = make_invoice(
            user=get_user_staff(),
            invoice_date=datetime.today(),
            contact=self.farm,
        )
        make_invoice_line(invoice, 1, 1.3, 'hours', 300.00, 0.20)
        make_invoice_line(invoice, 2, 2.4, 'hours', 200.23, 0.20)
        self.assertGreater(invoice.pk, 0)
        self.assertEqual(Decimal('1044.66'), invoice.gross)
        self.assertEqual(Decimal('870.55'), invoice.net)

    def test_get_first_line_number(self):
        """get the number for the first invoice line"""
        invoice = make_invoice(
            user=get_user_staff(),
            invoice_date=datetime.today(),
            contact=self.farm,
        )
        self.assertEqual(1, invoice.get_next_line_number())

    def test_get_next_line_number(self):
        """get the number for the next invoice line"""
        invoice = make_invoice(
            user=get_user_staff(),
            invoice_date=datetime.today(),
            contact=self.farm,
        )
        make_invoice_line(invoice, 2, 1.3, 'hours', 300.00, 0.20)
        self.assertEqual(3, invoice.get_next_line_number())

    def test_has_lines(self):
        """does the invoice have any lines"""
        invoice = make_invoice(
            user=get_user_staff(),
            invoice_date=datetime.today(),
            contact=self.farm,
        )
        make_invoice_line(invoice, 2, 1.3, 'hours', 300.00, 0.20)
        self.assertTrue(invoice.has_lines)

    def test_has_lines_not(self):
        invoice = make_invoice(
            user=get_user_staff(),
            invoice_date=datetime.today(),
            contact=self.farm,
        )
        self.assertFalse(invoice.has_lines)

    def test_user_can_edit(self):
        line = get_invoice_line_paperwork_no_time()
        self.assertTrue(line.user_can_edit)

    def test_user_can_edit_has_time(self):
        line = get_invoice_line_paperwork_has_time()
        self.assertFalse(line.user_can_edit)

    def test_user_can_edit_invoice(self):
        invoice = get_invoice_paperwork()
        InvoicePrint().create_pdf(invoice, None)
        line = get_invoice_line_paperwork_no_time()
        self.assertFalse(line.user_can_edit)
