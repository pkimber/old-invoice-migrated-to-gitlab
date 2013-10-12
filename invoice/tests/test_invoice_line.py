"""
Test invoice line
"""
from datetime import datetime
from datetime import time

from django.test import TestCase

from crm.tests.model_maker import (
    make_contact,
    make_priority,
    make_ticket,
)
from invoice.tests.model_maker import (
    make_invoice,
    make_invoice_line,
    make_time_record,
)
from login.tests.model_maker import make_user


class TestInvoiceLine(TestCase):

    def setUp(self):
        tom = make_user('tom')
        icl = make_contact('icl', 'ICL')
        invoice = make_invoice(
            tom,
            datetime.today(),
            icl,
        )
        self.invoice_line = make_invoice_line(
            invoice, 1, 1.3, 'hours', 300.00, 0.20
        )
        self.invoice_line_with_time = make_invoice_line(
            invoice, 2, 1.3, 'hours', 120.00, 0.20
        )
        ticket = make_ticket(
            icl,
            tom,
            'Sew',
            make_priority('Low', 1),
        )
        time_record = make_time_record(
            ticket,
            tom,
            'Set-up test framework',
            date_started=datetime(2012, 11, 13),
            start_time=time(9, 0),
            end_time=time(9, 30),
            billable=True,
        )
        time_record.invoice_line = self.invoice_line_with_time
        time_record.save()

    def test_has_time_record_not(self):
        self.assertFalse(self.invoice_line.has_time_record)

    def test_has_time_record(self):
        self.assertTrue(self.invoice_line_with_time.has_time_record)
