"""
Test invoice manager.
"""
from datetime import datetime
from datetime import time
from decimal import Decimal

from django.test import TestCase

from crm.tests.scenario import default_scenario_crm
from login.tests.scenario import (
    default_scenario_login,
    user_contractor,
)

from invoice.models import Invoice
#from invoice.tests.model_maker import (
#    make_invoice,
#    make_invoice_line,
#    make_time_record,
#)
from invoice.tests.scenario import (
    default_scenario_invoice,
    get_invoice_time_analysis,
)


class TestReport(TestCase):

    def setUp(self):
        self.line_number = 0
        user_contractor()
        default_scenario_login()
        default_scenario_crm()
        default_scenario_invoice()
        #invoice_settings()
        #self.invoice = make_invoice(
        #    get_user_staff(),
        #    datetime(2012, 3, 31),
        #    get_contact_farm()
        #)
        #self._make_line(1.0, get_user_web())
        #self._make_line(1.0, get_user_sara())
        #self._make_time(get_ticket_fence_for_farm(), 2.0, get_user_fred())
        #self._make_time(get_ticket_fence_for_farm(), 8.0, get_user_fred())
        #self._make_time(get_ticket_fence_for_farm(), 6.0, get_user_sara())
        #self._make_time(get_ticket_fix_roof_for_farm(), 14.0, get_user_sara())

    def test_report_total_by_user(self):
        invoice = get_invoice_time_analysis()
        result = invoice.time_analysis()
        import pprint
        pprint.pprint(result, indent=4)
        self.assertIn('fred', result)
        self.assertIn('sara', result)
        self.assertNotIn('web', result)
        net = Decimal()
        for user, tickets in result.items():
            for ticket_pk, totals in tickets.items():
                net = net + totals['net']
        self.assertEqual(invoice.net, net)
