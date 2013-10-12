"""
Test invoice line
"""
from django.test import TestCase

from invoice.models import (
    InvoiceLine,
)
from invoice.tests.scenario import (
    time_paperwork,
)
from crm.tests.scenario import (
    contact_contractor,
)
from login.tests.scenario import (
    user_contractor,
    user_default,
)


class TestInvoiceLine(TestCase):

    def setUp(self):
        user_contractor()
        user_default()
        contact_contractor()
        time_paperwork()

    def test_has_time_record_not(self):
        invoice_line = InvoiceLine.objects.get(units='pen')
        self.assertFalse(invoice_line.has_time_record)

    def test_has_time_record(self):
        invoice_line = InvoiceLine.objects.get(units='hours')
        self.assertTrue(invoice_line.has_time_record)
