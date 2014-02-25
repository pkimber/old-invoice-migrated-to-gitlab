# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime

from django.test import TestCase

from invoice.models import Invoice
from invoice.service import (
    InvoiceError,
    InvoicePrint,
)
from invoice.service import InvoiceCreate
from invoice.tests.model_maker import make_invoice
from invoice.tests.scenario import default_scenario_invoice
from crm.tests.scenario import (
    default_scenario_crm,
    get_contact_farm,
)
from login.tests.scenario import (
    default_scenario_login,
    get_user_staff,
    user_contractor,
)


class TestInvoicePrint(TestCase):

    def setUp(self):
        user_contractor()
        default_scenario_login()
        default_scenario_crm()
        default_scenario_invoice()

    def test_invoice_create_pdf(self):
        invoice = InvoiceCreate().create(
            get_user_staff(),
            get_contact_farm(),
            datetime(2013, 12, 31)
        )
        InvoicePrint().create_pdf(invoice, None)

    def test_invoice_create_pdf_no_lines(self):
        """Cannot create a PDF if the invoice has no lines"""
        invoice = make_invoice(
            user=get_user_staff(),
            invoice_date=datetime.today(),
            contact=get_contact_farm(),
        )
        self.assertRaises(
            InvoiceError,
            InvoicePrint().create_pdf,
            invoice,
            None
        )

    def test_invoice_create_pdf_not_draft(self):
        """Cannot create a PDF if the invoice has already been printed"""
        invoice = Invoice.objects.all()[0]
        InvoicePrint().create_pdf(invoice, None)
        self.assertRaises(
            InvoiceError,
            InvoicePrint().create_pdf,
            invoice,
            None
        )
