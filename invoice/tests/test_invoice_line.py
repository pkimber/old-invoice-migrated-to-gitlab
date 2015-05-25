# -*- encoding: utf-8 -*-
"""
Test invoice line
"""
from django.test import TestCase

from invoice.tests.factories import (
    InvoiceFactory,
    InvoiceLineFactory,
    TimeRecordFactory,
)
from invoice.models import InvoiceLine
#from invoice.tests.scenario import (
#    default_scenario_invoice,
#    get_timerecord_paperwork_template,
#)
from crm.tests.scenario import default_scenario_crm
from login.tests.scenario import (
    default_scenario_login,
    user_contractor,
)


class TestInvoiceLine(TestCase):

    def test_has_time_record_not(self):
        invoice_line = InvoiceLineFactory()
        self.assertFalse(invoice_line.has_time_record)

    def test_has_time_record(self):
        invoice_line = InvoiceLineFactory()
        time_record = TimeRecordFactory(invoice_line=invoice_line)
        self.assertTrue(invoice_line.has_time_record)
