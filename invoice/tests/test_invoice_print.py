from datetime import datetime
from datetime import time
from decimal import Decimal

from django.test import TestCase

from invoice.models import Invoice
from invoice.service import (
    InvoiceCreateBatch,
    InvoiceError,
    InvoicePrint,
)
from invoice.tests.model_maker import (
    make_invoice,
    make_invoice_settings,
    make_time_record,
)
from login.tests.model_maker import make_user
from login.tests.scenario import (
    get_user_staff,
    user_default,
)
from crm.tests.model_maker import (
    make_contact,
    make_priority,
    make_ticket,
)


VAT_RATE = Decimal('0.20')


class TestInvoicePrint(TestCase):

    def setUp(self):
        user_default()
        tom = make_user('tom')
        self.icl = make_contact(
            'icl',
            'ICL',
            address="130 High Street\nSheepwash\nHolsworthy\nEX2 3RF",
            hourly_rate=Decimal('20.00')
        )
        ticket = make_ticket(
            self.icl,
            tom,
            'Sew',
            make_priority('Low', 1),
        )
        make_time_record(
            ticket,
            tom,
            'Make a pillow case',
            datetime(2012, 9, 1),
            time(9, 0),
            time(12, 30),
            True
        )
        make_time_record(
            ticket,
            tom,
            'Buy a new sewing machine',
            datetime(2012, 9, 30),
            time(13, 30),
            time(15, 30),
            True
        )
        ticket_knit = make_ticket(
            self.icl,
            tom,
            'Knit',
            make_priority('Medium', 2),
        )
        make_time_record(
            ticket_knit,
            tom,
            'Make a nice cardigan',
            datetime(2012, 9, 1),
            time(10, 10),
            time(12, 30),
            True
        )
        make_invoice_settings(
            vat_rate=Decimal('0.20'),
            vat_number='',
            name_and_address='Patrick Kimber, Hatherleigh, EX20 1AB',
            phone_number='01234 234 456',
            footer="Please pay by bank transfer<br />For help, please phone<br />Thank you"
        )
        InvoiceCreateBatch().create(tom, datetime(2012, 9, 30))

    def test_invoice_create_pdf(self):
        invoice = Invoice.objects.all()[0]
        InvoicePrint().create_pdf(invoice, None)

    def test_invoice_create_pdf_no_lines(self):
        invoice = make_invoice(
            user=get_user_staff(),
            invoice_date=datetime.today(),
            contact=self.icl,
        )
        self.assertRaises(
            InvoiceError,
            InvoicePrint().create_pdf,
            invoice,
            None
        )

    def test_invoice_create_pdf_not_draft(self):
        invoice = Invoice.objects.all()[0]
        InvoicePrint().create_pdf(invoice, None)
        self.assertRaises(
            InvoiceError,
            InvoicePrint().create_pdf,
            invoice,
            None
        )
