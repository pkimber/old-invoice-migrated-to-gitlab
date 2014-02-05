"""
Test invoice line
"""
from django.test import TestCase

from invoice.models import InvoiceLine
from invoice.tests.scenario import (
    default_scenario_invoice,
    get_timerecord_paperwork_template,
)
from crm.tests.scenario import default_scenario_crm
from login.tests.scenario import (
    default_scenario_login,
    user_contractor,
)


class TestInvoiceLine(TestCase):

    def setUp(self):
        user_contractor()
        default_scenario_login()
        default_scenario_crm()
        default_scenario_invoice()

    def test_has_time_record_not(self):
        invoice_line = InvoiceLine.objects.get(units='pen')
        self.assertFalse(invoice_line.has_time_record)

    def test_has_time_record(self):
        time_record = get_timerecord_paperwork_template()
        invoice_line = InvoiceLine.objects.get(timerecord=time_record)
        self.assertTrue(invoice_line.has_time_record)
